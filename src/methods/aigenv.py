import gymnasium as gym
import numpy as np
import os
import timeit
from pathlib import Path
from gymnasium import spaces
from libs.yosysCmd import AigBase
from libs.abc_commands import ACTION_SPACE
from libs.cost_estimator import cost_estimator
from gymnasium.envs.registration import register

start = timeit.default_timer()

class AigEnv(AigBase, gym.Env):
    metadata = {'render_modes': ['human', 'system', 'none']}
    def __init__(self,
                 outdir: str,
                 cost_function: str,
                 action_num: int = 3,
                 timelimit: float = 60 * 60 * 3 - 60,
                 **kwargs
                 ):
        AigBase.__init__(self, outdir, cost_function, **kwargs)
        gym.Env.__init__(self)
        self.init()

        self.current_step = 1
        self.action_space = spaces.MultiDiscrete([len(ACTION_SPACE)]*action_num, dtype=np.int64)
        state, _ = self.take_step([0])
        self.state = state
        print("Initial state: ", state)
        self.obs_shape = (len(state), )
        self.observation_space = spaces.Box(low=0, high=min(max(state)*max(state),1e5), shape=self.obs_shape, dtype=np.int32)
        # print(self.observation_space)
        
        self.previous_cost = self.best_cost = self.run_best_cost = self.evaluate(self.aig_file)
        self.last_best_timestamp = timeit.default_timer()
        self.last_best_step = 0
        
        aig_file = self.aig_file
        if '.aig' in aig_file:
            filename = aig_file.split('.aig')[0]
        else:
            filename = aig_file
        self.new_aig_file = f"{filename}_new.aig"
        self.best_aig_file = f"{filename}_best.aig"
        self.timelimit = timelimit
        
        print("Initializing...")
        print("-----------------Initialized-----------------")
        print("Observation space: \t", self.observation_space)
        print("Action space: \t\t", self.action_space)
        
        
    def init(self):
        self.generate_optimized_lib(self.stdlib)
        self.get_module_names(self.netlist)
        # Convert the netlist to AIG format
        print("Converting netlist to AIG format...")
        self.verilog_to_aig(self.netlist)
        
    def reset(self, seed=None, *args, **kwargs):
        recover = os.path.exists(self.best_aig_file) and timeit.default_timer() - self.last_best_timestamp > 60 * 60
        if not recover:
            self.verilog_to_aig(self.netlist)
            
        if recover: self.save_best(self.best_aig_file, self.aig_file)
        cost = self.evaluate(self.aig_file)
        # best score does not reset
        self.previous_cost = self.run_best_cost = cost
        self.last_best_step = self.current_step
        state, _ = self.take_step([0])
        self.state = np.reshape(state, self.obs_shape).astype(np.int32)
        print(f'Reseting...')
        print(f'Current best: {self.best_cost}')
        print(f'Run best: {self.run_best_cost}')
        print(f'Current cost: {cost}')
        return self.state, {}
        
    def post_learning(self, aig_file: str, output):
        self.aig_to_netlist(output,  self.module_name, aig_file, f"{self.outdir}/lib/optimized_lib.lib" )
        # Estimate the cost of the optimized netlist
        cost = cost_estimator(output, self.stdlib, self.cost_function)
        return cost
    
    def evaluate(self, aig_file):
        self.aig_to_netlist(f"{self.outdir}/netlist.v", self.module_name, aig_file=aig_file, lib_file=f"{self.libDir}/optimized_lib.lib")
        cost = cost_estimator(f"{self.outdir}/netlist.v", self.stdlib, self.cost_function)
        return cost
        
    def __get_reward(self, cost: float):
        reward = self.previous_cost - cost
        # if self.current_step < 1000:
        #     if reward > 0:
        #         return 0
        #     else:
        #         return -0.01
        if reward > 0 and cost < self.best_cost:
            return reward
        return reward / 10
    
    def step(self, action):
        state, changed = self.take_step(action)
        self.current_step += 1
        # state = self.observation_space.sample()
        print(f'\rstep: {self.current_step}', end='')
        if self.current_step> 500 and self.current_step % 500 == 1:
            print()
        cost = self.evaluate(self.aig_file)
        
        if cost < self.run_best_cost:
            self.run_best_cost = cost
            print(f"\rImproving...{cost}", end='')
            self.last_best_timestamp = timeit.default_timer()
            self.last_best_step = self.current_step
            if self.run_best_cost < self.best_cost:
                self.best_cost = self.run_best_cost
                self.save_best(self.aig_file, self.best_aig_file)
                print(f"\rSaving Best... {cost}", end='')
            print()
        reward = self.__get_reward(cost)
        
        now = timeit.default_timer()
        done = now - start > self.timelimit
        truncate = self.current_step - self.last_best_step > len(self.ACTION_SPACE) * 3
        return np.reshape(state, self.obs_shape).astype(np.int32), reward, truncate, done , {'changed': changed , 'cost': cost}
    def render(self):
        pass
    def close(self):
        cost = self.evaluate(self.best_aig_file)
        print('Final cost: ', cost)
        return cost, self.last_best_timestamp - start

register(
     id="aigenv",
     entry_point="methods.aigenv:AigEnv",
     max_episode_steps=1e5,
)