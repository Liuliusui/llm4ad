

<div align="center">
<h1 align="center">
<img src="./assets/figs/logo.png" alt="LLM4AD Logo" style="width: 90%; height: auto;">
</h1>
<h1 align="center">
LLM4AD: Large Language Model for Algorithm Design
</h1>

[![Releases](https://img.shields.io/badge/Release-v1.0-blue)](https://github.com/Optima-CityU/LLM4AD/releases)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)
[![PR's Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Optima-CityU/LLM4AD/pulls)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
[![License](https://img.shields.io/badge/License-MIT-important)](https://github.com/Optima-CityU/LLM4AD/blob/main/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/llm4ad-doc/badge/?version=latest)](https://llm4ad-doc.readthedocs.io/en/latest/?badge=latest)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Optima-CityU/llm4ad/blob/main/example/online_bin_packing/bin_packing_funsearch.ipynb)

[Website](http://www.llm4ad.com/)
| [Documentation](https://llm4ad-doc.readthedocs.io/en/latest/)
| [Examples](https://github.com/Optima-CityU/LLM4AD/tree/main/example)
| [GUI](https://github.com/Optima-CityU/LLM4AD/tree/main/GUI)

</div>
<br>

## Introduction 📖

LLM4AD is an open-source Python-based Platform leveraging **Large Language Models (LLMs)** for **Automatic Algorithm Design (AD)**. 

LLM4AD is accomplished with [Documents](https://llm4ad-doc.readthedocs.io/en/latest/) and [Examples](https://github.com/Optima-CityU/LLM4AD/tree/main/example) materials to support users and developers to easily test, build and deploy their own LLM4AD applications and conduct research.

LLM4AD was originally developed for [optimisation tasks](https://llm4ad-doc.readthedocs.io/en/latest/task/optimization/index.html). The framework is versatile enough to be used in other areas, including [machine learning](https://llm4ad-doc.readthedocs.io/en/latest/task/machine_learning/index.html), [science discovery](https://llm4ad-doc.readthedocs.io/en/latest/task/science_discovery/index.html), game theory and engineering design.

For more information, see the [contact list](https://github.com/Optima-CityU/LLM4AD#Contact)

<img src="./assets/figs/framework.png" alt="llm4ad" style="zoom:50%;" />

## 🔥 News 

+ 2024.11 🎉🎉 **LLM4AD v1.0 Released**  ! 

+ 2024.10 🎉🎉 **Survey Paper** [“A Systematic Survey on Large Language Models for Algorithm Design”](https://arxiv.org/pdf/2410.14716) is online ! 

  

## 💡 Features of our package

| Feature                                                      | Support / To be supported |
| ------------------------------------------------------------ | ------------------------- |
| **Unified Interfaces** for methods                           | 🔥Support            |
| **Unified Interfaces** for tasks                             | 🔥Support             |
| **Unified Interfaces** for LLMs                              | 🔥Support             |
| **Evaluation acceleration:** multiprocessing evaluation, add Numba wrapper for heuristic | 🔥Support              |
| **Secure Evaluation:** main process protection, timeout interruption | 🔥Support             |
| **Logs:** local logs, Wandb and Tensorboard support          | 🔥Support             |
| **GUI:** methods selection, tasks selection, convergence, best algorithm, ... | 🔥Support             |
| **Resume run**                                               | 🚀Will be updated soon     |
| Support other languages                                      | 🚀Will be updated soon     |
| More search methods                                          | 🚀Will be updated soon     |
| More task examples                                           | 🚀Will be updated soon     |



## 🎁 Requirements & Installation

> [!Important]
> The Python version **must** be larger or equal to Python 3.9.


- refer to [requirements.txt](./requirements.txt)

- Numba (if you want to use Numba accelerate)

- Tensorboard (if you want to use a Tensorboard logger)

- wandb (if you want to use wandb logger)

- gym (if you want to try **Machine Learning** tasks)

- pandas (if you want to try **Science Discovery** tasks)

- all required packages in [requirements.txt](./requirements.txt) (if you want to use GUI)

  #### Install LLM4AD locally

  We suggest to install and run LLM4AD in [conda](https://conda.io/projects/conda/en/latest/index.html) env with python>=3.9, <=3.11

  ```bash
  cd LLM4AD
  
  pip install .
  ```

  #### Install LLM4AD using PiPy

  We suggest to install and run LLM4AD in [conda](https://conda.io/projects/conda/en/latest/index.html) env with python>=3.9, <=3.11

  ```bash
  pip install llm4ad
  ```

  

## 💻 Example Usage 

### Quick Start:

> [!Note]
> Configure your LLM api before running the script. For example:
>
> 1) Set `host`: 'api.deepseek.com'
> 2) Set `key`: 'your api key'
> 3) Set `model` `deepseek-chat'

```python
from llm4ad.task.optimization.online_bin_packing import OBPEvaluation
from llm4ad.tools.llm.llm_api_https import HttpsApi
from llm4ad.method.eoh import EoH, EoHProfiler


def main():

    llm = HttpsApi(host="xxx",  # your host endpoint, e.g., api.openai.com, api.deepseek.com
                   key="sk-xxx",  # your key, e.g., sk-xxxxxxxxxx
                   model="xxx",  # your llm, e.g., gpt-3.5-turbo, deepseek-chat
                   timeout=20)
    
    task = OBPEvaluation()

    method = EoH(llm=llm,
                 profiler=EoHProfiler(log_dir='logs/eoh', log_style='simple'),
                 evaluation=task,
                 max_sample_nums=20,
                 max_generations=10,
                 pop_size=4,
                 num_samplers=1,
                 num_evaluators=1, 
                 debug_mode=False)

    method.run()


if __name__ == '__main__':
    main()

```


### More Examples:
+ [Constructive Heuristics for TSP](https://github.com/Optima-CityU/LLM4AD/blob/main/example/tsp_construct/run_eoh.py)
+ [Constructive Heuristics for VRPTW](https://github.com/Optima-CityU/LLM4AD/blob/main/example/vrptw_construct/run_eoh.py)
+ ...
  

Check [Documents](https://llm4ad-doc.readthedocs.io/en/latest/index.html) for more tasks and examples

### GUI usage:

> [!Important]
> Install all required packages in [requirements.txt](./requirements.txt) for GUI usage

```bash
$ cd GUI
$ python run_gui.py
```

Check [GUI Introduction](https://llm4ad-doc.readthedocs.io/en/latest/getting_started/gui.html) for more information

<img src="./assets/figs/gui.gif" alt="llm4ad" style="zoom:80%;" />

## 📦 LLM4AD Search Methods

| Methods                                               | Paper title                                                  |
| ----------------------------------------------------- | ------------------------------------------------------------ |
| RandomSampling                                        | Understanding the Importance of Evolutionary Search in Automated Heuristic Design with Large Language Models (PPSN 2024) |
| FunSearch                                             | Mathematical Discoveries from Program Search with Large Language Models (Nature 2023) |
| EoH<font color=red>*</font>                           | Evolution of Heuristics: Towards Efficient Automatic Algorithm Design Using Large Language Model (ICML 2024) |
| (1+1)-EPS<font color=red>*</font> <br/>(HillClimbing) | Understanding the Importance of Evolutionary Search in Automated Heuristic Design with Large Language Models (PPSN 2024) |
| RegEvo                                                | coming soon                                                 |
| Neighborhood search methods                           | coming soon                                                 |
| Multi-objective search methods                        | coming soon                                                 |
| Others                                                | coming soon                                                 |

<font color=red>*</font>The implementation has some minor differences from the original method (demonstrated in their original paper), considering generality and multithreading acceleration.

## 📦LLM4AD Algorithm Design Tasks 


| Area              | Algorithm Task                                               | Paper                                             |
| ----------------- | ------------------------------------------------------------ | ------------------------------------------------- |
| Optimization      | [Online Bin Packing, Constructive heuristic]                 | [paper](https://openreview.net/pdf?id=BwAkaxqiLB) |
|                   | [Traveling Salesman Problem (TSP), Construct heuristic](https://llm4ad-doc.readthedocs.io/en/latest/task/optimization/tsp_construct.html) | [paper](https://arxiv.org/pdf/2311.15249)         |
|                   | Traveling Salesman Problem (TSP), Guided local search        | [paper](https://openreview.net/pdf?id=BwAkaxqiLB) |
|                   | Flow Shop Scheduling Problem (FSSP), Guided local search     | [paper](https://openreview.net/pdf?id=BwAkaxqiLB) |
|                   | Bayesian Optimization, Cost-aware Acquisition Function Design | [paper](https://arxiv.org/abs/2404.16906)         |
| Machine Learning  | Adversarial Attack, Attack strategy                          | [paper](https://arxiv.org/abs/2401.15335)         |
|                   | [Acrobot, Heuristic (Agent)](https://llm4ad-doc.readthedocs.io/en/latest/task/machine_learning/acrobot.html) |                                                   |
|                   | [Cart Pole, Heuristic (Agent)](https://llm4ad-doc.readthedocs.io/en/latest/task/machine_learning/car_pole.html) |                                                   |
|                   | [Mountain Car, Heuristic (Agent)](https://llm4ad-doc.readthedocs.io/en/latest/task/machine_learning/mountain_car.html) |                                                   |
| Science Discovery | Computational fluid dynamics, Turbulence model design        | [paper](https://arxiv.org/pdf/2410.10657)         |
|                   | [Bacteria Growth, Function](https://llm4ad-doc.readthedocs.io/en/latest/task/science_discovery/bacteria_grow.html) |                                                   |
|                   | [Oscillator, Equation](https://llm4ad-doc.readthedocs.io/en/latest/task/science_discovery/oscillator1.html) |                                                   |
|                   | [Stress & Strain, Equation](https://llm4ad-doc.readthedocs.io/en/latest/task/science_discovery/stress_strain.html) |                                                   |
| Math              | Admissible Sets                                              | [paper](https://www.nature.com/articles/s41586-023-06924-6)                                                  |
| coming soon ...   |                                                              |                                                   |



## 🤖 LLM Interfaces
There are three approaches on LLM interface implementation, check [Tutorial on LLM interface implementation](https://llm4ad-doc.readthedocs.io/en/latest/dev/llm.html) for more information.
+ **Remote LLM API** (e.g., GPT4o, GPT3.5, Gemini Pro, Deepseek ...) (**<Recommended !!!>**)
+ **Local HuggingFace LLM Deployment** (e.g., Llamacode, Llama, Gemma, Deepseek, ...)
+ **Your Implementation** If you want to use your own GPT API or local LLMs deployment, please create and add your interface in [LLM](https://github.com/Optima-CityU/LLM4AD/tree/main/llm4ad/tools/llm)



## 🗎 Tutorial: How to Use LLM4AD to Solve Your Algorithm Design Task

A Step-by-step Tutorial on using LLM4AD to solve your algorithm design task is provided [here](https://llm4ad-doc.readthedocs.io/en/latest/dev/run_new_task.html#)




## 🪪 Licence

This project is licensed under the **MIT License** - see the [LICENSE](./LICENSE) file for details. Parts of this project use code licensed under the Apache License 2.0.



## ✨Reference 

If you find LLM4AD helpful please cite:

```bibtex
Coming soon
```



## About LLM4AD

This platform is developed and maintained by LLM4AD developer group from the City University of Hong Kong (CityUHK) and the Southern University of Science and Technology (SUSTech). We develop LLM4AD platform for research purposes and hope to contribute to the research area by delivering tools for LLM-based algorithm design methods.

+ **Contribution:** We are more than welcome to contribute including developing code and ideas to improve our platform.
+ **Collaborations:** If you like our platform, and you would like to use it for profit-making purposes? We are always searching for industrial collaborations because they help direct research to meet the industry’s needs.
+ **Issue:** If you find a bug or you have any kind of concern regarding the correctness, please report us an issue.
+ **Profit Purpose:** If you intend to use LLM4AD for any profit-making purposes, please contact [us](http://www.llm4ad.com/contact.html).



## Contact

If you are interested in LLM4AD or if you encounter any difficulty using the platform, you can:

1. Visit our website [LLM4AD Web](http://www.llm4ad.com)

2. Visit our collection [a collection of resources and research papers on LLM4AD](https://github.com/FeiLiu36/LLM4Opt)

3. Join our QQ Group

   <img src="./assets/figs/qq.png" alt="LLM4AD Logo" style="width: 30%; height: auto;">

4. Contact us through email fliu36-c@my.cityu.edu.hk

5. Submit an [issue](https://github.com/Optima-CityU/LLM4AD)



