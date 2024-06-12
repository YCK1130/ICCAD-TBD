import os
import subprocess
import platform
from libs.utils import parse_lib, parse_netlist, TmpDir, seperate_lines
from libs.libgen import gate_cost_estimator, generate_lib_file
from libs.cost_estimator import cost_estimator
from pathlib import Path
import numpy as np
import json
import math
import random
import timeit
# Determine current architecture and set paths for Yosys and ABC
arch = platform.machine()
print(f"Current architecture: {arch}")

if arch == 'arm64':
    yosys = os.path.abspath('../binary_arm64/yosys')
    abc_binary = os.path.abspath('../binary_arm64/yosys-abc')
elif arch == 'x86_64':
    yosys = os.path.abspath('../binary_x86/yosys')
    abc_binary = os.path.abspath('../binary_x86/yosys-abc')
else:
    raise Exception("Unsupported architecture")

# Check if binaries exist and are executable
for binary in [yosys, abc_binary]:
    if not os.path.isfile(binary) or not os.access(binary, os.X_OK):
        raise Exception(f"Binary not found or not executable: {binary}")

# Set ABC_COMMAND environment variable
os.environ['ABC_COMMAND'] = abc_binary
print(f"ABC_COMMAND set to: {os.environ['ABC_COMMAND']}")

class AigBase:
    def __init__(self,
                 *, 
                 outdir: str,
                 netlist: str = None,
                 cost_function:str,
                 stdlib: str = None
                 ) -> None:
        self.outdir = outdir
        self.parseDir = f'{outdir}/parsed'
        self.aigerDir = f'{outdir}/aigers'
        self.libDir = f'{self.outdir}/lib'
        for d in [self.parseDir, self.aigerDir, self.libDir]:
            Path(d).mkdir(parents=True, exist_ok=True)
        
        self.netlist = netlist
        self.cost_function = cost_function
        self.stdlib = stdlib
        self.module_name = None
        
    def get_module_names(self, verilog_file):
        yosys_script = f"read_verilog {verilog_file}; hierarchy -auto-top; ls;"
        yosys_command = [yosys, '-p', yosys_script]
        try:
            output = subprocess.check_output(yosys_command, stderr=subprocess.STDOUT).decode()
            self.module_name = self.parse_module_names(output)
            return self.parse_module_names(output)
        except subprocess.CalledProcessError as e:
            print(f"Error running Yosys: {e.output.decode()}")
            raise
    def parse_module_names(self, yosys_output):
        module_name = ""
        for line in yosys_output.split('\n'):
            if line.startswith("Top module:"):
                module_name = line.split(":")[1].strip()
        return module_name
    def verilog_to_aig(self, verilog_file, aig_file):
        proc = subprocess.check_output([yosys, "-p", f"read_verilog {verilog_file}; aigmap; write_aiger {aig_file}"])
        lines = seperate_lines(proc)
        
    def improve_aig(self, aig_file: str, commands: list):
        if '.aig' in aig_file:
            filename = aig_file.split('.aig')[0]
        else:
            filename = aig_file
        new_aig_file = f"{filename}_new.aig"
        assert isinstance(commands, list)
        abc_command = f"read_aiger {aig_file}; {'; '.join(commands)};cec {aig_file}; write_aiger {new_aig_file}"
        proc = subprocess.check_output([abc_binary, "-q", abc_command], stderr=subprocess.STDOUT)
        results = seperate_lines(proc)
        if 'Networks are equivalent' in results[-1]:
            Path(new_aig_file).replace(aig_file)

    def improve_aig_simulated_annealing(self, aig_file: str, commands: list, temperature, cooling_rate):
        if '.aig' in aig_file:
            filename = aig_file.split('.aig')[0]
        else:
            filename = aig_file
        new_aig_file = f"{filename}_new.aig"

        i = 0
        start = timeit.default_timer()
        # run the optimization once to set the initial energy (cost) of the system
        print('Initializing annealing ..')
        print('Current temperature: ' + str(temperature))
        print('----------------')
        self.aig_to_netlist(aig_file, f"{self.libDir}/optimized_lib.lib", f"{self.outdir}/netlist.v", self.module_name)
        cost = cost_estimator(f"{self.outdir}/netlist.v", self.stdlib, self.cost_function)
        current_design_file = aig_file
        previous_cost = cost
        i += 1
        print('System initialized with cost: ' + str(cost))
        print('Starting annealing ..')
        print()
        while True:
            number_of_accepted_optimizations = 0

            for _ in range(100):
                # if we accept 10 optimizations, we cool down the system
                # otherwise, only continue up to 100 trials for this temperature
                print('Iteration: ' + str(i))
                print('Temperature: ' + str(temperature))
                print('Current cost: ' + str(previous_cost))
                print('----------------')
            
            
                # Pick an optimization at random
                # random_optimization = random.choice(optimizations)
                abc_command = f"read_aiger {current_design_file}; {'; '.join(np.random.choice(commands, 3))};cec {current_design_file}; write_aiger {new_aig_file}"
                proc = subprocess.check_output([abc_binary, "-q", abc_command], stderr=subprocess.STDOUT)
                results = seperate_lines(proc)
                if 'Networks are equivalent' in results[-1]:
                    nxt_design_file = new_aig_file

                self.aig_to_netlist(nxt_design_file, f"{self.libDir}/optimized_lib.lib", f"{self.outdir}/netlist.v", self.module_name)
                cost = cost_estimator(f"{self.outdir}/netlist.v", self.stdlib, self.cost_function)
                

                # if better than the previous cost, accept. Otherwise, accept with probability
                if cost < previous_cost:
                    print('The optimization reduced the cost!')
                    print('Accepting it ..')
                    print('Cost reduced from ' + str(previous_cost) + ' to ' + str(cost))
                    current_design_file = nxt_design_file
                    previous_cost = cost
                    number_of_accepted_optimizations += 1
                else:
                    delta_cost = cost - previous_cost
                    probability_of_acceptance = math.exp((- delta_cost) / temperature)
                    print('The optimization didn\'t reduce the cost, the system looks to be still hot.')
                    print('The probability of acceptance is: ' + str(probability_of_acceptance))
                    print('Uniformly generating a number to see if we accept it ..')
                    if random.uniform(0, 1.0) < probability_of_acceptance:
                        print('Accepting it ..')
                        current_design_file = nxt_design_file
                        previous_cost = cost
                        number_of_accepted_optimizations += 1
                    else:
                        print('Rejected ..')
                        pass
                i += 1
                print()

                if number_of_accepted_optimizations == 10:
                    break

            if temperature <= 0.1:
                print('System has sufficiently cooled down ..')
                print('Shutting down simulation ..')
                print()
                break

            new_temperature = temperature * cooling_rate
            print('Cooling down system from ' + str(temperature) + ' to ' + str(new_temperature) + ' ..')
            temperature = new_temperature
            print('================')
            print()

        stop = timeit.default_timer()
        Path(new_aig_file).replace(aig_file)
        print('Total Optimization Time: ' + str(stop - start))
        
    def aig_to_netlist(self, aig_file, lib_file, netlist_file, module_name):
        proc = subprocess.check_output([yosys, "-p", f"read_aiger {aig_file}; abc -exe {abc_binary} -liberty {lib_file}; clean; rename -top {module_name[1:]}; write_verilog -noattr {netlist_file}"])
        # lines = seperate_lines(proc)
    def generate_optimized_lib(self, library: str):
        with open(library, 'r') as f:
            lib = json.load(f)
        data = parse_lib(lib)
        print("All libraries parsed successfully!")
        with TmpDir(self.parseDir):
            print(f"Writing to {self.parseDir}/test.json")
            with open(f"{self.parseDir}/test.json", 'w') as f:
                json.dump(data, f, indent=4)
            
            print(f"Reading Netlist from {self.netlist}")
            with open(self.netlist, 'r') as f:
                netlist_str = f.read()
            cleaned_netlist = parse_netlist(netlist_str)
            print(f"Writing to {self.parseDir}/netlist_cleaned.v")
            with open(f"{self.parseDir}/netlist_cleaned.v", 'w') as f:
                f.write(cleaned_netlist)
            # Generate a list of best pairs(gate names, min costs) for each gate type
            name_cost = gate_cost_estimator(f"{self.parseDir}/test.json", library, self.cost_function)
            print("All gate costs estimated successfully!")
            # Generate the optimized lib file with the name_cost pairs
            print(f"Writing to {self.libDir}/optimized_lib.lib")
            generate_lib_file(name_cost, f"{self.libDir}/optimized_lib.lib")