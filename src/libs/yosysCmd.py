import os
import subprocess
import platform
from libs.utils import parse_lib, parse_netlist, TmpDir, seperate_lines, replace_assign_with_buffer_in_file
from libs.libgen import gate_cost_estimator, generate_lib_file
from libs.abc_commands import ACTION_SPACE
from pathlib import Path
import numpy as np
import json
import shutil
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
                 outdir: str,
                 cost_function:str,
                 netlist: str = None,
                 aig_file:str = None,
                 lib_file:str = None,
                 stdlib: str = None,
                 **kwargs
                 ) -> None:
        self.outdir = outdir
        self.parseDir = f'{self.outdir}/parsed'
        self.aigerDir = f'{self.outdir}/aigers'
        self.libDir = f'{self.outdir}/lib'
        
        for d in [self.parseDir, self.aigerDir, self.libDir]:
            Path(d).mkdir(parents=True, exist_ok=True)
        
        self.netlist = netlist
        self.cost_function = cost_function
        self.stdlib = stdlib
        self.module_name = None
        
        self.aig_file = aig_file if aig_file != None else  f"{self.aigerDir}/netlist.aig"
        self.lib_file = lib_file if lib_file != None else  f"{self.libDir}/optimized_lib.lib"
        self.ACTION_SPACE = ACTION_SPACE
        self.state = None
        self.name_cost = None
        
    def get_module_names(self, verilog_file):
        yosys_script = f"read_verilog {verilog_file}; hierarchy -auto-top; ls;"
        yosys_command = [yosys, '-p', yosys_script]
        try:
            output = subprocess.check_output(yosys_command, stderr=subprocess.STDOUT).decode()
            self.module_name = self.parse_module_names(output)
            return self.module_name
        except subprocess.CalledProcessError as e:
            print(f"Error running Yosys: {e.output.decode()}")
            raise
    def parse_module_names(self, yosys_output):
        module_name = ""
        for line in yosys_output.split('\n'):
            if line.startswith("Top module:"):
                module_name = line.split(":")[1].strip()
        return module_name
    def verilog_to_aig(self, verilog_file, aig_file=None):
        if aig_file == None: aig_file = self.aig_file
        proc = subprocess.check_output([yosys, "-p", f"read_verilog {verilog_file}; aigmap; write_aiger {aig_file}"])
        lines = seperate_lines(proc)
        
    def improve_aig(self, aig_file: str, commands: list, replace: bool = True)-> bool:
        '''
        @return Boolean indicating whether state change
        '''
        if '.aig' in aig_file:
            filename = aig_file.split('.aig')[0]
        else:
            filename = aig_file
        new_aig_file = f"{filename}_new.aig"
        assert isinstance(commands, list) or isinstance(commands, np.ndarray)
        # if need more information please append after this, and you should handle it in 'extract_state'
        get_states = ' ; '.join(['ps', 'print_supp']) 
        abc_command = f"read_aiger {aig_file}; {'; '.join(commands)}; {get_states} ; write_aiger {new_aig_file}"
        try:
            proc = subprocess.check_output([abc_binary, "-q", abc_command], stderr=subprocess.STDOUT)
        except:
            return False
        results = seperate_lines(proc)
        
        # print(abc_command)
        state = self.extract_state(results, get_states)
        # # for Debug
        # for line in results:
        #     print(line)
        if not isinstance(self.state, (list, np.ndarray)) or (len(state) == len(self.state) and 
            any([state[i] != self.state[i] for i in range(len(state))])):
            if replace:
                self.state = state
                Path(new_aig_file).replace(aig_file)
            return True
        return False

    def aig_to_netlist(self, netlist_file, module_name, aig_file=None, lib_file=None):
        if aig_file == None: aig_file = self.aig_file
        if lib_file == None: lib_file = self.lib_file
        proc = subprocess.check_output([yosys, "-p", f"read_aiger {aig_file}; abc -exe {abc_binary} -liberty {lib_file}; clean; rename -top {module_name[1:]}; write_verilog -noattr {netlist_file}"])
        for cell_name, cost in self.name_cost:
            gate_type = cell_name.split('_')[0]
            if(gate_type == 'buf'):
                replace_assign_with_buffer_in_file(netlist_file, cell_name)
                break;
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
            self.name_cost = name_cost
            print("All gate costs estimated successfully!")
            # Generate the optimized lib file with the name_cost pairs
            print(f"Writing to {self.lib_file}")
            generate_lib_file(name_cost, self.lib_file)
    
    @staticmethod       
    def extract_state(raw_state: list[str], get_states_cmd: str)-> list[int] :
        cmds = get_states_cmd.split(' ; ')
        cmds = [c.strip() for c in cmds]
        
        states = []
        PIs = POs = None
        while any([exclude in raw_state[0] for exclude in ['Warning','Performing renoding with choices.']]):
            raw_state.pop(0)
        for cmd in cmds:
            if cmd == 'ps':
                stats = raw_state.pop(0).split(':\x1b[0m')[-1].split(' ')
                stats = [ s for s in stats if s!='']
                # [i, o, lat, and, lev]
                assert stats[0] == 'i/o', [raw_state, states]
                # i
                PIs = int(stats[2].split('/')[0])
                states.append(PIs)
                # o
                POs = int(stats[3])
                states.append(POs)
                # lat
                states.append(int(stats[6]))
                # and
                states.append(int(stats[9]))
                # lev
                try:
                    lev = int(stats[12])
                except:
                    print(stats)
                    raise
                states.append(lev)
                # print(states)
            elif cmd == 'print_supp':
                assert PIs != None and POs != None, 'You should set vitals status first!'
                raw_state.pop(0)
                stats = raw_state[:POs]
                del raw_state[:POs]
                for stat in stats:
                    stat = stat.split(':')[-1].split('(')[0].strip().split('.')
                    stat = [s.split('=')[-1].strip() for s in stat if s.strip()!='']
                    stat = [int(s) for s in stat]
                    states += stat
                    # print(stat)
        return states
    
    def take_step(self, action: int | list[int], aig_file=None):
        if aig_file==None:
            aig_file = self.aig_file
        if isinstance(action, list) or isinstance(action, np.ndarray):
            commands = [self.ACTION_SPACE[i] for i in action if 0 <= i and i < len(self.ACTION_SPACE)]
        elif isinstance(action, int) and 0 <= action and action < len(self.ACTION_SPACE):
            commands = [self.ACTION_SPACE[action]]
        changed = self.improve_aig(aig_file, commands)
        return self.state, changed
    
    def save_best(self, source:str, target:str):
        shutil.copy(source, target)