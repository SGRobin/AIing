import pickle
import Simulation.env_create as env

file_path = "C:\\Users\\USER\\PycharmProjects\\AIing\\robot_network_1.pkl"

# Now, you can load the instance back from the file
with open(file_path, "rb") as file:
    loaded_network = pickle.load(file)\

env.load_simulation(True)
env.run_simulation(loaded_network, True, 2000)
env.unload_simulation()
