import os
import subprocess
import platform
from libs.utils import seperate_lines
from pathlib import Path
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

def get_module_names(verilog_file):
    yosys_script = f"read_verilog {verilog_file}; hierarchy -auto-top; ls;"
    yosys_command = [yosys, '-p', yosys_script]
    try:
        output = subprocess.check_output(yosys_command, stderr=subprocess.STDOUT).decode()
        return parse_module_names(output)
    except subprocess.CalledProcessError as e:
        print(f"Error running Yosys: {e.output.decode()}")
        raise

def parse_module_names(yosys_output):
    module_name = ""
    for line in yosys_output.split('\n'):
        if line.startswith("Top module:"):
            module_name = line.split(":")[1].strip()
    return module_name

def verilog_to_aig(verilog_file, aig_file):
    module_name = get_module_names(verilog_file)
    proc = subprocess.check_output([yosys, "-p", f"read_verilog {verilog_file}; aigmap; write_aiger {aig_file}"])
    lines = seperate_lines(proc)
    return module_name
    
def improve_aig(aig_file: str, commands: list):
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
    
def aig_to_netlist(aig_file, lib_file, netlist_file, module_name):
    proc = subprocess.check_output([yosys, "-p", f"read_aiger {aig_file}; abc -exe {abc_binary} -liberty {lib_file}; clean; rename -top {module_name[1:]}; write_verilog -noattr {netlist_file}"])
    # lines = seperate_lines(proc)
