import json
from pathlib import Path


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


class TmpDir:
    def __init__(self, tmp_dir: Path):
        self.tmp_dir = tmp_dir

    def __enter__(self):
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        return self.tmp_dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"Error: {exc_val}")
            print(f"Traceback: {exc_tb}")
        self.tmp_dir.rmdir()
