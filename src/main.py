import argparse
import numpy as np
from methods.simulated_annealing import Simulated_Annealing
from methods.fast_simulated_annealing import Fast_Simulated_Annealing
from methods.greedy import Greedy
from libs.abc_commands import ACTION_SPACE


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
    parser.add_argument('--method', '-m', type=str, default='sa',
                        help='Optimization method: Simulated_Annealing (sa), greedy')
    return parser.parse_args()

SEED = 1234
np.random.seed(SEED)
if __name__ == "__main__":
    args = parse_args()
    temperature = 3
    cooling_rate = 0.9

    if args.method.lower() not in ['simulated_annealing', 'simulated annealing', 'sa', 'greedy', 'fsa']:
        raise f'Unknown method {args.method}'
    if args.method.lower() == 'greedy':
        agent = Greedy(args.outdir,
                        args.cost_function,
                        aig_file=f"{args.outdir}/aigers/netlist.aig",
                        netlist=args.netlist,
                        stdlib = args.library
                        )
    elif args.method.lower() == 'fsa':
        agent = Fast_Simulated_Annealing(
            args.outdir,
            args.cost_function,
            aig_file=f"{args.outdir}/aigers/netlist.aig",
            netlist=args.netlist,
            stdlib = args.library,
        )
    else: 
        agent = Simulated_Annealing(args.outdir,
                                    args.cost_function,
                                    aig_file=f"{args.outdir}/aigers/netlist.aig",
                                    netlist=args.netlist,
                                    stdlib = args.library,
                                    temperature=temperature,
                                    cooling_rate=cooling_rate
                                    )
    agent.init()
    
    # Simmulated Annealing Version
    print("Improving...")
    # for i in tqdm.trange(10):
        # commands = np.random.choice(ACTION_SPACE, 10)
    # agent.learn(f"{args.outdir}/aigers/netlist.aig", ACTION_SPACE, temperature=temperature ,cooling_rate=cooling_rate, 
    #             recover = False, verbose=1)
    cost, found_time, total_time = agent.learn(f"{args.outdir}/aigers/netlist.aig", ACTION_SPACE, verbose=1)

    # cost = agent.post_learning(f"{args.outdir}/aigers/netlist_best.aig", args.output)
    cost = agent.post_learning(f"{args.outdir}/aigers/netlist_best.aig", args.output)
    print(f"Final cost: {cost}")
    with open(f"{args.outdir}/results.txt" , 'w') as f:
        f.write(f"Final cost: {cost}\n")
        f.write(f"Total Time: {total_time}\n")
        f.write(f"Found Time: {found_time}\n")
        # f.writelines([f"Final cost: {cost}", f"Found Time: {found_time}", f"Total Time: {total_time}"])

# sample command: 
# python3 main.py -library ../release/lib/lib1.json -netlist ../release/netlists/design1.v -cost_function ../release/cost_estimators/cost_estimator_1