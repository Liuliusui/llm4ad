# Module Name: FunSearch
# Last Revision: 2025/2/16
# This file is part of the LLM4AD project (https://github.com/Optima-CityU/llm4ad).
#
# Reference:
#   - Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog, M. Pawan Kumar, Emilien Dupont, Francisco JR Ruiz et al. 
#       "Mathematical discoveries from program search with large language models." 
#       Nature 625, no. 7995 (2024): 468-475.
# 
# ------------------------------- Copyright --------------------------------
# Copyright (c) 2025 Optima Group.
# 
# Permission is granted to use the LLM4AD platform for research purposes. 
# All publications, software, or other works that utilize this platform 
# or any part of its codebase must acknowledge the use of "LLM4AD" and 
# cite the following reference:
# 
# Fei Liu, Rui Zhang, Zhuoliang Xie, Rui Sun, Kai Li, Xi Lin, Zhenkun Wang, 
# Zhichao Lu, and Qingfu Zhang, "LLM4AD: A Platform for Algorithm Design 
# with Large Language Model," arXiv preprint arXiv:2412.17287 (2024).
# 
# For inquiries regarding commercial use or licensing, please contact 
# http://www.llm4ad.com/contact.html
# --------------------------------------------------------------------------

from __future__ import annotations

import concurrent.futures
import time
from threading import Thread
import traceback
from typing import Optional, Literal

from . import programs_database
from .config import ProgramsDatabaseConfig
from ...base import *
from .profiler import FunSearchProfiler
from ...tools.profiler import ProfilerBase


class FunSearch:
    def __init__(self,
                 llm: LLM,
                 evaluation: Evaluation,
                 profiler: ProfilerBase = None,
                 num_samplers: int = 4,
                 num_evaluators: int = 4,
                 samples_per_prompt: int = 4,
                 max_sample_nums: Optional[int] = 20,
                 *,
                 resume_mode: bool = False,
                 debug_mode: bool = False,
                 multi_thread_or_process_eval: Literal['thread', 'process'] = 'thread',
                 **kwargs):
        """Function Search.
        Args:
            template_program: the seed program (in str) as the initial function of the run.
                the template_program should be executable, i.e., incorporating package import, and function definition, and function body.
            llm             : an instance of 'llm4ad.base.LLM', which provides the way to query LLM.
            evaluation      : an instance of 'llm4ad.base.Evaluator', which defines the way to calculate the score of a generated function.
            profiler        : an instance of 'llm4ad.method.funsearch.FunSearchProfiler'. If you do not want to use it, you can pass a 'None'.
            max_sample_nums : terminate after evaluating max_sample_nums functions (no matter the function is valid or not).
            num_samplers    : number of independent Samplers in the experiment.
            num_evaluators  : number of independent program Evaluators in the experiment.
            resume_mode     : in resume_mode, funsearch will not evaluate the template_program, and will skip the init process. TODO: More detailed usage.
            debug_mode      : if set to True, we will print detailed information.
            multi_thread_or_process_eval: use 'concurrent.futures.ThreadPoolExecutor' or 'concurrent.futures.ProcessPoolExecutor' for the usage of
                multi-core CPU while evaluation. Please note that both settings can leverage multi-core CPU. As a result on my personal computer (Mac OS, Intel chip),
                setting this parameter to 'process' will faster than 'thread'. However, I do not sure if this happens on all platform so I set the default to 'thread'.
                Please note that there is one case that cannot utilize multi-core CPU: if you set 'safe_evaluate' argument in 'evaluator' to 'False',
                and you set this argument to 'thread'.
            **kwargs        : some args pass to 'llm4ad.base.SecureEvaluator'. Such as 'fork_proc'.
        """
        # arguments and keywords
        self._template_program_str = evaluation.template_program
        self._max_sample_nums = max_sample_nums
        self._num_samplers = num_samplers
        self._num_evaluators = num_evaluators
        self._samples_per_prompt = samples_per_prompt
        self._debug_mode = debug_mode
        self._resume_mode = resume_mode

        # function to be evolved
        self._function_to_evolve: Function = TextFunctionProgramConverter.text_to_function(self._template_program_str)
        self._function_to_evolve_name: str = self._function_to_evolve.name
        self._template_program: Program = TextFunctionProgramConverter.text_to_program(self._template_program_str)

        # population, sampler, and evaluator
        self.db_config = ProgramsDatabaseConfig()
        self._database = programs_database.ProgramsDatabase(
            self.db_config,
            self._template_program,
            self._function_to_evolve_name
        )
        self._sampler = SampleTrimmer(llm)
        llm.debug_mode = debug_mode
        self._evaluator = SecureEvaluator(evaluation, debug_mode=debug_mode, **kwargs)
        self._profiler = profiler

        if profiler is not None:
            self._profiler.record_parameters(llm, evaluation, self)  # ZL: Necessary

        # statistics
        self._tot_sample_nums = 0

        # multi-thread executor for evaluation
        assert multi_thread_or_process_eval in ['thread', 'process']
        if multi_thread_or_process_eval == 'thread':
            self._evaluation_executor = concurrent.futures.ThreadPoolExecutor(
                max_workers=self._num_evaluators
            )
        else:
            self._evaluation_executor = concurrent.futures.ProcessPoolExecutor(
                max_workers=self._num_evaluators
            )

        # threads for sampling
        self._sampler_threads = [
            Thread(target=self._sample_evaluate_register) for _ in range(self._num_samplers)
        ]

    def _sample_evaluate_register(self):
        while (self._max_sample_nums is None) or (self._tot_sample_nums < self._max_sample_nums):
            try:
                # get prompt
                prompt = self._database.get_prompt()
                prompt_contents = [prompt.code for _ in range(self._samples_per_prompt)]

                # do sample
                draw_sample_start = time.time()
                sampled_funcs = self._sampler.draw_samples(prompt_contents)
                draw_sample_times = time.time() - draw_sample_start
                avg_time_for_each_sample = draw_sample_times / len(sampled_funcs)

                # convert samples to program instances
                programs_to_be_eval = []
                for func in sampled_funcs:
                    program = SampleTrimmer.sample_to_program(func, self._template_program)
                    # if sample to program success
                    if program is not None:
                        programs_to_be_eval.append(program)

                # submit tasks to the thread pool and evaluate
                futures = []
                for program in programs_to_be_eval:
                    future = self._evaluation_executor.submit(self._evaluator.evaluate_program_record_time, program)
                    futures.append(future)
                # get evaluate scores and evaluate times
                scores_times = [f.result() for f in futures]
                scores, times = [i[0] for i in scores_times], [i[1] for i in scores_times]

                # register to program database and profiler
                island_id = prompt.island_id
                for program, score, eval_time in zip(programs_to_be_eval, scores, times):
                    # update
                    self._tot_sample_nums += 1
                    # convert to Function instance
                    function = TextFunctionProgramConverter.program_to_function(program)
                    # check if the function has converted to Function instance successfully
                    if function is None:
                        continue
                    # register to program database
                    if score is not None:
                        self._database.register_function(
                            function=function,
                            island_id=island_id,
                            score=score
                        )
                    # register to profiler
                    if self._profiler is not None:
                        function.score = score
                        function.sample_time = avg_time_for_each_sample
                        function.evaluate_time = eval_time
                        self._profiler.register_function(function)
                        if isinstance(self._profiler, FunSearchProfiler):
                            self._profiler.register_program_db(self._database)
            except KeyboardInterrupt:
                break
            except Exception as e:
                if self._debug_mode:
                    traceback.print_exc()
                    exit()
                continue

        # shutdown evaluation_executor
        try:
            self._evaluation_executor.shutdown(cancel_futures=True)
        except:
            pass

    def run(self):
        if not self._resume_mode:
            # evaluate the template program, make sure the score of which is not 'None'
            score, eval_time = self._evaluator.evaluate_program_record_time(program=self._template_program)
            if score is None:
                raise RuntimeError('The score of the template function must not be "None".')

            # register the template program to the program database
            self._database.register_function(function=self._function_to_evolve, island_id=None, score=score)
            if self._profiler:
                self._function_to_evolve.score = score
                self._function_to_evolve.evaluate_time = eval_time
                self._profiler.register_function(self._function_to_evolve)

        # start sampling using multiple threads
        for t in self._sampler_threads:
            t.start()

        # join all threads to the main thread
        for t in self._sampler_threads:
            t.join()

        if self._profiler is not None:
            self._profiler.finish()
