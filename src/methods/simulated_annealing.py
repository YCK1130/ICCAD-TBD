import math
import random
import timeit
import os
import subprocess
import tqdm
import numpy as np
from libs.utils import parse_lib, parse_netlist, TmpDir, seperate_lines
from libs.yosysCmd import AigBase
from libs.cost_estimator import cost_estimator
from pathlib import Path


class Simulated_Annealing(AigBase):
    def __init__(self,
                 outdir: str,
                 cost_function: str,
                 temperature: float = 3.0,
                 cooling_rate: float = 0.9,
                 **kwargs
                 ) -> None:
        super().__init__(
            outdir,
            cost_function,
            **kwargs)
        self.temperature = temperature
        self.cooling_rate = cooling_rate
    def init(self):
        self.generate_optimized_lib(self.stdlib)
        self.get_module_names(self.netlist)
        # Convert the netlist to AIG format
        print("Converting netlist to AIG format...")
        self.verilog_to_aig(self.netlist)
        
    def post_learning(self, aig_file: str, output):
        self.aig_to_netlist(output,  self.module_name, aig_file, f"{self.outdir}/lib/optimized_lib.lib", )
        # Estimate the cost of the optimized netlist
        cost = cost_estimator(output, self.stdlib, self.cost_function)
        return cost
    
    def learn(self, aig_file: str, commands: list, temperature=None, cooling_rate=None, recover=False, verbose=0):
        if '.aig' in aig_file:
            filename = aig_file.split('.aig')[0]
        else:
            filename = aig_file
        new_aig_file = f"{filename}_new.aig"
        best_aig_file = f"{filename}_best.aig"
        self.save_best(aig_file, best_aig_file)
        
        if temperature == None: temperature=self.temperature
        if cooling_rate == None: cooling_rate=self.cooling_rate

        i = 0
        start = timeit.default_timer()
        best_time = timeit.default_timer()
        # run the optimization once to set the initial energy (cost) of the system
        if verbose > 0:
            print('Initializing annealing ..')
            print('Current temperature: ' + str(temperature))
            print('----------------')
        
        self.aig_to_netlist(f"{self.outdir}/netlist.v", self.module_name, aig_file=best_aig_file if recover else aig_file, lib_file=f"{self.libDir}/optimized_lib.lib")
        cost = cost_estimator(f"{self.outdir}/netlist.v", self.stdlib, self.cost_function)
        # current_design_file = aig_file
        # nxt_design_file = new_aig_file
        previous_cost = best_cost = cost
        best_iter = 0
        i += 1
        if verbose > 0:
            print('System initialized with cost: ' + str(cost))
            print('Starting annealing ..')
            print()
        while True:
            number_of_accepted_optimizations = 0

            for _trial in range(100):
                # if we accept 10 optimizations, we cool down the system
                # otherwise, only continue up to 100 trials for this temperature
                if verbose > 1 or (verbose == 1 and _trial % 10 == 0):
                    print('Iteration: ' + str(i))
                    print('Temperature: ' + str(temperature))
                    print('Current cost: ' + str(previous_cost))
                    print('Current best: ' + str(best_cost) + f' (stored at {best_iter})')
                    print('----------------')
            
            
                # Pick an optimization at random
                # random_optimization = random.choice(optimizations)
                # abc_command = f"read_aiger {current_design_file}; {'; '.join(np.random.choice(commands, 3))};cec {current_design_file}; write_aiger {new_aig_file}"
                # proc = subprocess.check_output([abc_binary, "-q", abc_command], stderr=subprocess.STDOUT)
                # results = seperate_lines(proc)
                
                changed = self.improve_aig(aig_file, list(np.random.choice(commands, min(3, len(commands)))), replace=False)
                nxt_design_file = new_aig_file
                if changed:
                    self.aig_to_netlist( f"{self.outdir}/netlist.v", self.module_name, aig_file=nxt_design_file, lib_file=f"{self.libDir}/optimized_lib.lib" )
                    cost = cost_estimator(f"{self.outdir}/netlist.v", self.stdlib, self.cost_function)
                else:
                    cost = previous_cost

                # if better than the previous cost, accept. Otherwise, accept with probability
                if cost < previous_cost:
                    if verbose > 1:
                        print('The optimization reduced the cost!')
                        print('Accepting it ..')
                        print('Cost reduced from ' + str(previous_cost) + ' to ' + str(cost))
                    # current_design_file = nxt_design_file
                    Path(new_aig_file).replace(aig_file)
                    previous_cost = cost
                    number_of_accepted_optimizations += 1
                elif cost > previous_cost:
                    delta_cost = cost - previous_cost
                    probability_of_acceptance = math.exp((- delta_cost) / temperature)
                    if verbose > 1:
                        print('The optimization didn\'t reduce the cost, the system looks to be still hot.')
                        print('The probability of acceptance is: ' + str(probability_of_acceptance))
                        print('Uniformly generating a number to see if we accept it ..')
                    if random.uniform(0, 1.0) < probability_of_acceptance:
                        if verbose > 1:
                            print('Accepting it ..')
                        # current_design_file = nxt_design_file
                        Path(new_aig_file).replace(aig_file)
                        previous_cost = cost
                        number_of_accepted_optimizations += 1
                    else:
                        if verbose > 1:
                            print('Rejected ..')
                        pass
                if cost < best_cost:
                    self.save_best(aig_file, best_aig_file)
                    best_cost = cost
                    best_iter = number_of_accepted_optimizations
                    best_time = timeit.default_timer()
                i += 1
                if verbose > 1:
                    print()

                if number_of_accepted_optimizations == 10:
                    break

            if temperature <= 0.1:
                if verbose > 0:    
                    print('System has sufficiently cooled down ..')
                    print('Shutting down simulation ..')
                    print()
                break

            new_temperature = temperature * cooling_rate
            if verbose > 0:
                print('Cooling down system from ' + str(temperature) + ' to ' + str(new_temperature) + ' ..')
                print('================')
                print()
            temperature = new_temperature

        stop = timeit.default_timer()
        if verbose > 0:
            print('Total Optimization Time: ' + str(stop - start))
        return best_cost, best_time - start, stop - start