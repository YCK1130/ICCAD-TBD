import json
import subprocess
import tqdm
import argparse
import numpy as np
from libs.utils import parse_lib, parse_netlist, TmpDir
from libs.libgen import gate_cost_estimator, generate_lib_file
from libs.yosysCmd import verilog_to_aig, aig_to_netlist, improve_aig
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

    with open(args.library, 'r') as f:
        lib = json.load(f)
    data = parse_lib(lib)
    print("All libraries parsed successfully!")
    with TmpDir(f'{args.outdir}/parsed'):
        print(f"Writing to {args.outdir}/parsed/test.json")
        if not Path(args.outdir).exists():
            Path(args.outdir).mkdir(parents=True, exist_ok=True)
        with open(f"{args.outdir}/parsed/test.json", 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"Reading Netlist from {args.netlist}")
        with open(args.netlist, 'r') as f:
            netlist_str = f.read()
        cleaned_netlist = parse_netlist(netlist_str)
        print(f"Writing to {args.outdir}/parsed/netlist_cleaned.v")
        with open(f"{args.outdir}/parsed/netlist_cleaned.v", 'w') as f:
            f.write(cleaned_netlist)

        # Generate a list of best pairs(gate names, min costs) for each gate type
        name_cost = gate_cost_estimator(f"{args.outdir}/parsed/test.json", args.library, args.cost_function)
        print("All gate costs estimated successfully!")

        # Generate the optimized lib file with the name_cost pairs
        print(f"Writing to {args.outdir}/lib/optimized_lib.lib")
        if not Path(f'{args.outdir}/lib').exists():
            Path(f'{args.outdir}/lib').mkdir(parents=True, exist_ok=True)
        generate_lib_file(name_cost, f"{args.outdir}/lib/optimized_lib.lib")

    # Convert the netlist to AIG format
    print("Converting netlist to AIG format...")
    if not Path(f'{args.outdir}/aigers').exists():
            Path(f'{args.outdir}/aigers').mkdir(parents=True, exist_ok=True)
    module_name = verilog_to_aig(args.netlist, f"{args.outdir}/aigers/netlist.aig")

    print("Improving...")


    for i in tqdm.trange(1000):
        commands = np.random.choice(ACTION_SPACE, 1)
        improve_aig(f"{args.outdir}/aigers/netlist.aig", [c for c in commands])
        # Convert the AIG to netlist with the optimized lib
        # print("Converting AIG to netlist...")
    aig_to_netlist(f"{args.outdir}/aigers/netlist.aig", f"{args.outdir}/lib/optimized_lib.lib", args.output, module_name)

    # Estimate the cost of the optimized netlist
    cost = cost_estimator(args.output, args.library, args.cost_function)
        # print(f"{command} cost: {cost}")
        
    print(f"Final cost: {cost}")
    
# sample command: 
# python3 main.py -library ../release/lib/lib1.json -netlist ../release/netlists/design1.v -cost_function ../release/cost_estimators/cost_estimator_1