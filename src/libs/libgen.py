import json
import subprocess
import tqdm
from utils import parse_lib, parse_netlist
import argparse
from pathlib import Path

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

def gate_cost_estimator(libPath, cost_estimator):
    with open(libPath, 'r') as f:
        lib = json.load(f)
    for cell in lib['types']:
        if(cell != 'buf' and cell != 'not'):
            for cell_name in lib['types'][cell]:
                generate_2_input_verilog_file(cell_name, f'../../data/verilog/{cell_name}.v')
                proc = subprocess.check_output([cost_estimator, ' -library', libPath, ' -netlist ', f'../../data/verilog/{cell_name}.v', ' -output ', f'../../data/cost/{cell_name}.out'])
                line = proc.decode("utf-8").split('\n')
                print(line)
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
    gate_cost_estimator('../../data/parsed/test.json', '../../release/cost_estimators/cost_estimator_1')
    # new_names_areas = [
    #     ('buf_1', 7),
    #     ('not_1', 3.5),
    #     ('nand_1', 4.5),
    #     ('nor_1', 4.2),
    #     ('or_1', 4.8),
    #     ('and_1', 4.1),
    #     ('xor_1', 5.2),
    #     ('xnor_1', 5.5)
    # ]
    # output_filename = 'generated_example.lib'

    # generate_lib_file(new_names_areas, output_filename)
