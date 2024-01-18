import pickle

import necessities
import testing.xor_agent as xor_agent
import robot_agent

import Simulation.env_create as env

env.load_simulation(True)
print(env.run_simulation(None, False, 10000, False, True))
env.unload_simulation()