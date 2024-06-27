This is a project for 2024 ICCAD constest and finl project for IEDA@NTU, TW.

# Netlist Optimization Framework

This repository contains a framework for optimizing logic synthesis using various methods, including Reinforcement Learning (RL), Simulated Annealing, Fast Simulated Annealing, and Greedy algorithms. The framework is designed to generate an optimized library (.lib) and convert unprocessed netlists (.v) into AIG files, which are then optimized and mapped back to primitive gate netlists.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Methods](#methods)

## Introduction

The optimization process begins with generating an optimized library based on the gates listed in the original library. Primitive gate netlists are created and sent to a black-box cost estimator. Based on the returned costs, gates of the same type are ranked, and the optimized library is completed for later use during mapping.

The given unprocessed netlist (.v) is converted into an AIG file using Yosys and yosys-abc binary files executed through Python's subprocess package. An optimization algorithm is applied to this AIG circuit, and the optimized AIG circuit is mapped back to the primitive gates netlist using the optimized library. The netlist is then sent to the cost estimator to determine if the process should terminate. If not, the cost and AIG circuit are updated, and the algorithm continues running until the optimized netlist with the minimum cost is achieved.

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/YCK1130/ICCAD-TBD.git
   cd ICCAD-TBD
2.	Ensure you have Yosys and yosys-abc installed:
    ```sh
    sudo apt-get install yosys
## Usage
Move to the the directory containing main.py
```sh 
cd src
```
Run the main.py script with the appropriate arguments:
```sh 
python3 main.py -library <path_to_library_json> -netlist <path_to_netlist_v> -cost_function <path_to_cost_function> -output <path_to_output_netlist_v>
```
Example:
```sh
python3 main.py -library ../release/lib/lib1.json -netlist ../release/netlists/design1.v -cost_function ../release/cost_estimators/cost_estimator_1 -output design_optimized.v
```
## Methods

The framework supports several optimization methods:

- sa (Simulated Annealng): A probabilistic technique for approximating the global optimum of a given function.
- fsa (Fast Simulated Annealing): A faster variant of simulated annealing.
- greedy (Greedy): A simple, heuristic-based optimization method.

```sh 
python3 main.py -library <path_to_library_json> -netlist <path_to_netlist_v> -cost_function <path_to_cost_function> -output <path_to_output_netlist_v> --method <method>
```
Example:
```sh
python3 main.py -library ../release/lib/lib1.json -netlist ../release/netlists/design1.v -cost_function ../release/cost_estimators/cost_estimator_1 -output design_optimized.v --method sa
```

