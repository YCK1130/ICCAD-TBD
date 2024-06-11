import json
import subprocess
import tqdm
import argparse
import numpy as np
from libs.utils import parse_lib, parse_netlist, TmpDir
from libs.libgen import gate_cost_estimator, generate_lib_file
from libs.yosysCmd import AigBase
from libs.cost_estimator import cost_estimator
from libs.abc_commands import ACTION_SPACE
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

    agent = AigBase(outdir = args.outdir, netlist=args.netlist, cost_function=args.cost_function)
    agent.generate_optimized_lib(args.library)
    module_name = agent.get_module_names(args.netlist)
    # Convert the netlist to AIG format
    print("Converting netlist to AIG format...")
    agent.verilog_to_aig(args.netlist, f"{args.outdir}/aigers/netlist.aig")

    print("Improving...")
    for i in tqdm.trange(10):
        commands = np.random.choice(ACTION_SPACE, 1)
        agent.improve_aig(f"{args.outdir}/aigers/netlist.aig", [c for c in commands])
    
    agent.aig_to_netlist(f"{args.outdir}/aigers/netlist.aig", f"{args.outdir}/lib/optimized_lib.lib", args.output, module_name)
    # Estimate the cost of the optimized netlist
    cost = cost_estimator(args.output, args.library, args.cost_function)
        # print(f"{command} cost: {cost}")
    print(f"Final cost: {cost}")
    
# sample command: 
# python3 main.py -library ../release/lib/lib1.json -netlist ../release/netlists/design1.v -cost_function ../release/cost_estimators/cost_estimator_1