import os
import signal
import sys

import timeit
import argparse
import numpy as np
import gymnasium as gym
import torch
from stable_baselines3 import A2C
from methods.simulated_annealing import Simulated_Annealing
from libs.abc_commands import ACTION_SPACE, DRILL_SPACE
from pathlib import Path
from methods.aigenv import AigEnv

def parse_args():
    all_required = False
    parser = argparse.ArgumentParser(
        description='We aim to optimize a netlist with...')
    parser.add_argument('-library', type=str, default='lib.json', required=all_required,
                        help='Path to the libraries json file')
    parser.add_argument('-netlist', type=str, default='design.v', required=all_required,
                        help='Path to the netlist file')
    parser.add_argument('-cost_function', type=str, default='cost_function_1', required=all_required,
                        help='Cost function to optimize')
    parser.add_argument('-output', type=str, default='design_optimized.v', required=all_required,
                        help='Path to the output optimized netlist file')
    parser.add_argument('--outdir', '-od', type=str, default='../data',
                        help='Path to the output directory')
    return parser.parse_args()

SEED = 1234
np.random.seed(SEED)
if __name__ == "__main__":
    args = parse_args()
    
    start = timeit.default_timer()

    env = gym.make('aigenv', 
                   outdir=args.outdir,
                   cost_function=args.cost_function,
                   aig_file=f"{args.outdir}/aigers/netlist.aig",
                   netlist=args.netlist,
                   stdlib = args.library,
                   )
    model = A2C("MlpPolicy", env, verbose=1, device='cpu', 
                learning_rate= 1e-5,
                policy_kwargs = {
                    'net_arch' : [16, 16],
                    'activation_fn': torch.nn.ReLU
                })
    print("---------------Model---------------")
    print(model.policy)
    print("-----------------------------------")
    def sigint_handler(signal, frame):
        print("Interrupted!")
        cost, found_time = env.close()
        finish = timeit.default_timer()
        with open(f"{args.outdir}/results.txt" , 'w') as f:
            f.write(f"Final cost: {cost}\n")
            f.write(f"Found Time: {found_time}\n")
            f.write(f"Total Time: {finish - start}\n")
        sys.exit(0)
    signal.signal(signal.SIGINT, sigint_handler)
    
    model.learn(total_timesteps=25000)
    model.save(f"{args.outdir}/a2c_final")

    cost, found_time = env.close()
    finish = timeit.default_timer()
    with open(f"{args.outdir}/results.txt" , 'w') as f:
        f.write(f"Final cost: {cost}\n")
        f.write(f"Found Time: {found_time}\n")
        f.write(f"Total Time: {finish - start}\n")
# sample command: 
# python3 main.py -library ../release/lib/lib1.json -netlist ../release/netlists/design1.v -cost_function ../release/cost_estimators/cost_estimator_1