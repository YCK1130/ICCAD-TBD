import json
import subprocess
import tqdm
import argparse
from pathlib import Path

def generate_1_input_verilog_file(gate_name, output_filename):
    # Define the header of the .v file
    verilog_header = """module top_809960632_810038711_1598227639_893650103(a, o);
    input a;
    output o;
"""

    # Initialize content with the header
    verilog_content = [verilog_header]

    # Create instance for the given gate name
    instance = f"    {gate_name} g0(a, o);\n"
    verilog_content.append(instance)

    # Close the module
    verilog_content.append("endmodule\n")

    # Join the content into a single string
    final_content = ''.join(verilog_content)

    # Write the content to the output file
    with open(output_filename, 'w') as file:
        file.write(final_content)

def generate_2_input_verilog_file(gate_name, output_filename):
    # Define the header of the .v file
    verilog_header = """module top_809960632_810038711_1598227639_893650103(a, b, o);
    input a, b;
    output o;
"""
    # Initialize content with the header
    verilog_content = [verilog_header]

    # Create instance for the given gate name
    instance = f"    {gate_name} g0(a, b, o);\n"
    verilog_content.append(instance)

    # Close the module
    verilog_content.append("endmodule\n")

    # Join the content into a single string
    final_content = ''.join(verilog_content)

    # Write the content to the output file
    with open(output_filename, 'w') as file:
        file.write(final_content)

def gate_cost_estimator(parsedLib:str, oriLib, cost_estimator):
    name_cost = []
    with open(parsedLib, 'r') as f:
        lib = json.load(f)
    baseDir = "/".join(parsedLib.split('/')[:-1])
    Path(f'{baseDir}/verilog').mkdir(parents=True, exist_ok=True)
    Path(f'{baseDir}/cost').mkdir(parents=True, exist_ok=True)
        
    for cell in lib['types']:
        name_cost.append((cell, 0))
        for cell_name in lib['types'][cell]:
            # print(cell_name)
            if(cell != 'buf' and cell != 'not'):
                generate_2_input_verilog_file(cell_name, f'{baseDir}/verilog/{cell_name}.v')
            else:
                generate_1_input_verilog_file(cell_name, f'{baseDir}/verilog/{cell_name}.v')
            proc = subprocess.check_output([cost_estimator, '-library', f'{oriLib}', '-netlist', f'{baseDir}/verilog/{cell_name}.v', '-output', f'{baseDir}/cost/{cell_name}.out'])
            line = proc.decode("utf-8").split('\n')
            cost = float(line[0].split('=')[1].strip())
            # print(cost)
            if name_cost[-1][1] > cost or not name_cost[-1][1]:
                name_cost[-1] = (cell_name, cost)
    subprocess.run([f'rm -rf {baseDir}/verilog/*'], shell=True)
    subprocess.run([f'rm -rf {baseDir}/cost/*'], shell=True)
    return name_cost
    # return data

def generate_lib_file(new_names_areas, output_filename):
    # Define the header of the .lib file
    lib_header = """// Generated Liberty File
/* This is an auto-generated .lib file */
library(demo) {
"""

    # Initialize content with the header
    lib_content = [lib_header]

    # Define the template for each cell
    cell_template = """    cell({cell_name}) {{
        area: {area};
        pin(Y) {{
            direction: output;
            function: "{function}";
        }}
{input_pins}
    }}

"""

    # Define the functions and input pins for each gate type
    functions_and_pins = {
        "buf": ("A", "        pin(A) { direction: input; }"),
        "not": ("A'", "        pin(A) { direction: input; }"),
        "nand": ("(A*B)'", "        pin(A) { direction: input; }\n        pin(B) { direction: input; }"),
        "nor": ("(A+B)'", "        pin(A) { direction: input; }\n        pin(B) { direction: input; }"),
        "or": ("A+B", "        pin(A) { direction: input; }\n        pin(B) { direction: input; }"),
        "and": ("A*B", "        pin(A) { direction: input; }\n        pin(B) { direction: input; }"),
        "xor": ("A ^ B", "        pin(A) { direction: input; }\n        pin(B) { direction: input; }"),
        "xnor": ("(A ^ B)'", "        pin(A) { direction: input; }\n        pin(B) { direction: input; }")
    }

    # Iterate over the provided names and areas
    for cell_name, area in new_names_areas:
        gate_type = cell_name.split('_')[0]
        if gate_type in functions_and_pins:
            function, input_pins = functions_and_pins[gate_type]
            cell_content = cell_template.format(
                cell_name=cell_name,
                area=area,
                function=function,
                input_pins=input_pins
            )
            lib_content.append(cell_content)

    # Close the library
    lib_content.append("}\n")

    # Join the content into a single string
    final_content = ''.join(lib_content)

    # Write the content to the output file
    with open(output_filename, 'w') as file:
        file.write(final_content)

if __name__ == "__main__":
    name_cost = gate_cost_estimator('../../data/parsed/test.json', '../../release/lib/lib1.json', '../../release/cost_estimators/cost_estimator_1')
    output_filename = 'generated_example.lib'

    generate_lib_file(name_cost, output_filename)
