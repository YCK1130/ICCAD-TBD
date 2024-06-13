# import math
# import random
import timeit
# import os
# import subprocess
# import tqdm
# import numpy as np
# from libs.utils import parse_lib, parse_netlist, TmpDir, seperate_lines
from libs.yosysCmd import AigBase
from libs.cost_estimator import cost_estimator
from pathlib import Path
        

class Greedy(AigBase):
    def __init__(self,
                 outdir: str,
                 cost_function: str,
                 **kwargs
                 ) -> None:
        super().__init__(
            outdir,
            cost_function,
            **kwargs)
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
    
    def learn(self, aig_file: str, commands: list):
        if '.aig' in aig_file:
            filename = aig_file.split('.aig')[0]
        else:
            filename = aig_file
        new_aig_file = f"{filename}_new.aig"
        best_aig_file = f"{filename}_best.aig"

        start = timeit.default_timer()
        best_time = timeit.default_timer()
        previous_cost = float('inf')
        i = 0
        while True:
            print('Iteration: ' + str(i))
            print('Current cost: ' + str(previous_cost))
            print('-------------')
            
            ### 1 ###
            # run every command and choose the best one
            # results = Parallel(n_jobs=len(optimizations))(delayed(run_thread)(iteration_dir, current_design_file, opt) for opt in optimizations)
            cmd_best_cost = previous_cost         
            for cmd in commands:
                # print('Running command: ' + cmd)
                # cmd_best_cost = previous_cost
                changed = self.improve_aig(aig_file, [cmd], replace=False)
                # print(changed)
                if changed:
                    # print('changed the state:)')
                    self.aig_to_netlist( f"{self.outdir}/netlist.v", self.module_name, aig_file=new_aig_file, lib_file=f"{self.libDir}/optimized_lib.lib" )
                    cost = cost_estimator(f"{self.outdir}/netlist.v", self.stdlib, self.cost_function)
                    # print('Cost: ' + str(cost))
                    if cost < cmd_best_cost:
                        # print('cost = ' + str(cost) + ' < cmd_best_cost = ' + str(cmd_best_cost))
                        cmd_best_cost = cost
                        self.save_best(new_aig_file, best_aig_file)
                        best_cmd = cmd
                # else:
                    # print('didn\'t change the state:(')
    
            ### 2 ###
            #  compare the best cost among iterations
            if cmd_best_cost < previous_cost:
                # print('This iteration reduced the cost!!')
                print('Choosing command ' + best_cmd + ' -> cost from: ' + str(previous_cost) +' to ' + str(cmd_best_cost))
                previous_cost = cmd_best_cost
            
                # update design file for the next iteration
                # Path(best_aig_file).replace(aig_file)
                self.save_best(best_aig_file, aig_file)
                best = timeit.default_timer()
                i += 1
                # print('================')
                # print()
            else:
                print('This iteration didn\'t reduce the cost:(')
                break   
            
        stop = timeit.default_timer()

        print('best Time: ' + str(best - start))
        print('run Time: ' + str(stop - start))
        # Path(best_aig_file).replace(aig_file)    
        return cmd_best_cost, best_time - start, stop - start
        

        