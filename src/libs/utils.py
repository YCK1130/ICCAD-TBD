import json
from pathlib import Path

import re

def replace_assign_with_buffer_in_file(input_file, buffer_name):
    # Read the Verilog file
    with open(input_file, 'r') as file:
        verilog_code = file.read()
    
    # Define the pattern to match `assign a = b;`
    pattern = r'assign\s+(\w+)\s*=\s*(\w+)\s*;'
    
    # Initialize a counter for unique buffer names
    buffer_counter = 1
    
    # Function to replace matched pattern with buffer gate
    def replace_match(match):
        nonlocal buffer_counter
        a = match.group(1)
        b = match.group(2)
        # Create a unique buffer gate name
        buffer_name = f"_buffer{buffer_counter}"
        buffer_counter += 1
        return f'buf_8 {buffer_name} (\n   .A({b}),\n   .Y({a})\n   );'
    
    # Replace all matches in the input Verilog code
    new_verilog_code = re.sub(pattern, replace_match, verilog_code)
    
    # Write the transformed Verilog code to the output file
    with open(input_file, 'w') as file:
        file.write(new_verilog_code)

def dict_append(d: dict, key: str, value: any) -> dict:
    if key in d:
        d[key].append(value)
    else:
        d[key] = [value]
    return d


def parse_lib(lib: dict) -> dict:
    assert 'information' in lib and 'cells' in lib, 'Invalid lib format'
    '''Parse the library to a more readable format
    Input:
        lib: dict
    Output:
        data: {
            'info': dict,
            'types': {
                'cell_type': [cell_name]
            },
            'cells': [{
                'cell_name',
                'cell_type', 
                ...
            }]
        }
    '''
    data = {}
    data['information'] = lib['information']
    data['types'] = {}
    data['cells'] = {}
    lib_cells = lib['cells']
    for cell in lib_cells:
        dict_append(data['types'], cell['cell_type'], cell['cell_name'])
        data['cells'][cell['cell_name']] = cell
    return data


def parse_netlist(netlist_str: str) -> dict:
    netlist = netlist_str.replace('\n', '').replace(
        '\t', '').split(';')
    netlist = [line.strip() for line in netlist if line.strip()]
    head = netlist[0].replace('module', '\nmodule')
    end = netlist[-1]
    wires = []
    inputs = []
    outputs = []
    gates = []
    for line in netlist[1:-1]:
        if 'wire' in line:
            wires.append(line.split(' ')[1])
        elif 'input' in line:
            inputs.append(line.split(' ')[1])
        elif 'output' in line:
            outputs.append(line.split(' ')[1])
        else:
            gates.append(line.replace('    ', ' ').replace('  ', ' '))

    cleaned_netlist = '{head};\n\tinput {inputs};\n\toutput {outputs};\n\twire {wires};\n\t{gates};\n{end}'.format(
        head=head, wires=', '.join(wires),
        inputs=', '.join(inputs), outputs=', '.join(outputs),
        gates=';\n\t'.join(gates), end=end)
    return cleaned_netlist

def seperate_lines(lines: str)-> list[str]:
    try:
        return lines.decode("utf-8").strip().split('\n')
    except Exception as e:
        print(f"Error running [seperate_lines]: {e}")
        raise

class TmpDir:
    def __init__(self, tmp_dir: Path):
        if isinstance(tmp_dir, str):
            tmp_dir = Path(tmp_dir)
        self.tmp_dir = tmp_dir

    def __enter__(self):
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        return self.tmp_dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"Error: {exc_val}")
            print(f"Traceback: {exc_tb}")
        for file in self.tmp_dir.iterdir():
            file.unlink(missing_ok=True)
        self.tmp_dir.rmdir()
