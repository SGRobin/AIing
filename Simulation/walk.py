import pickle
import Simulation.env_create as env

file_path = "C:\\Users\\USER\\PycharmProjects\\AIing\\networks\\save_network_generation.pkl"

# Now, you can load the instance back from the file
with open(file_path, "rb") as file:
    loaded_network = pickle.load(file)\

env.load_simulation(True)
print(env.run_simulation(loaded_network, True, 1000))
env.unload_simulation()
