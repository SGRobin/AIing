import pickle
import Simulation.env_create as env

# file_path = "..\\networks\\walk.4.29.pkl"
# file_path = "..\\networks\\save_network_generation.pkl"
file_path = "..\\save_network_0.pkl"

with open(file_path, "rb") as file:
    loaded_network = pickle.load(file)


simulation = env.Simulation(True)
# print(simulation.run_simulation(loaded_network, True, 3000, False))
print(simulation.run_simulation(loaded_network, True, 3000))
simulation.unload_simulation()
