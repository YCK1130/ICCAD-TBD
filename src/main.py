import json
import subprocess
import tqdm
from libs.utils import parse_lib, parse_netlist
from libs.libgen import gate_cost_estimator, generate_lib_file
import argparse
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
    parser.add_argument('--outdir', '-od', type=str, default='../data/parsed/',
                        help='Path to the output directory')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    with open(args.library, 'r') as f:
        lib = json.load(f)
    data = parse_lib(lib)
    if not Path(args.outdir).exists():
        Path(args.outdir).mkdir(parents=True, exist_ok=True)
    with open(f"{args.outdir}/test.json", 'w') as f:
        json.dump(data, f, indent=4)
    print("All libraries parsed successfully!")
    print(f"Writing to {args.outdir}/test.json")

    with open(args.netlist, 'r') as f:
        netlist_str = f.read()
    cleaned_netlist = parse_netlist(netlist_str)
    with open(f"{args.outdir}/netlist_cleaned.v", 'w') as f:
        f.write(cleaned_netlist)

    name_cost = gate_cost_estimator(f"{args.outdir}/test.json", args.library, args.cost_function)
    print("All gate costs estimated successfully!")
    generate_lib_file(name_cost, f"../data/lib/optimized_lib.lib")
    print(f"Writing to ../data/lib/optimized_lib.lib successfully!")

# sample command: 
# python3 main.py -library ../release/lib/lib1.json -netlist ../release/netlists/design1.v -cost_function ../release/cost_estimators/cost_estimator_1