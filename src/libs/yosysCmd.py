import subprocess

def verilog_to_aig(verilog_file, aig_file):
    subprocess.run(["yosys",f"read_verilog {verilog_file}; aigmap; write_aiger -s {aig_file}"], check=True)