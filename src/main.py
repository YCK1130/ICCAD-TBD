import json
import subprocess
import tqdm
import argparse
import numpy as np
from methods.simulated_annealing import Simulated_Annealing
from methods.greedy import Greedy
from libs.abc_commands import ACTION_SPACE, DRILL_SPACE
from pathlib import Path


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
    temperature = 3
    cooling_rate = 0.9

    # agent = Simulated_Annealing(args.outdir,
    #                             args.cost_function,
    #                             aig_file=f"{args.outdir}/aigers/netlist.aig",
    #                             netlist=args.netlist,
    #                             stdlib = args.library,
    #                             temperature=temperature,
    #                             cooling_rate=cooling_rate
    #                             )
    agent = Greedy(args.outdir,
                                args.cost_function,
                                aig_file=f"{args.outdir}/aigers/netlist.aig",
                                netlist=args.netlist,
                                stdlib = args.library
                                )
    agent.init()
    
    # Simmulated Annealing Version
    print("Improving...")
    # for i in tqdm.trange(10):
        # commands = np.random.choice(ACTION_SPACE, 10)
    # agent.learn(f"{args.outdir}/aigers/netlist.aig", ACTION_SPACE, temperature=temperature ,cooling_rate=cooling_rate, 
    #             recover = False, verbose=1)
    agent.learn(f"{args.outdir}/aigers/netlist.aig", ACTION_SPACE)

    # cost = agent.post_learning(f"{args.outdir}/aigers/netlist_best.aig", args.output)
    cost = agent.post_learning(f"{args.outdir}/aigers/netlist_best.aig", args.output)
    print(f"Final cost: {cost}")
    
# sample command: 
# python3 main.py -library ../release/lib/lib1.json -netlist ../release/netlists/design1.v -cost_function ../release/cost_estimators/cost_estimator_1