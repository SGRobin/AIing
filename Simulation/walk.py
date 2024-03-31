import pickle
import Simulation.env_create as env

# file_path = "..\\networks\\robot_network.pkl"
# file_path = "..\\networks\\save_network_generation.pkl"
file_path = "..\\save_network_0.pkl"

# Now, you can load the instance back from the file
with open(file_path, "rb") as file:
    loaded_network = pickle.load(file)

# env.load_simulation(True)
# print(env.run_simulation(loaded_network, False, 1000))
# print(env.run_simulation(loaded_network, False, 1000))
# print(env.run_simulation(loaded_network, False, 1000))
# print(env.run_simulation(loaded_network, False, 1000))
# print(env.run_simulation(loaded_network, False, 1000))
# env.unload_simulation()
simulation = env.Simulation(True)
# print(simulation.run_simulation(loaded_network, True, 3000, False))
print(simulation.run_simulation(loaded_network, True, 3000))
simulation.unload_simulation()
