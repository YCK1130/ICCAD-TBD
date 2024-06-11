import subprocess

def cost_estimator(verilog_file, lib_file, estimator):
    proc = subprocess.check_output([estimator, '-library', f'{lib_file}', '-netlist', f'{verilog_file}', '-output', f'../data/cost/result.out'])
    line = proc.decode("utf-8").split('\n')
    cost = float(line[0].split('=')[1].strip())
    return cost