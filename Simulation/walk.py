import pickle
import Simulation.env_create as env

file_path = "C:\\Users\\USER\\PycharmProjects\\AIing\\networks\\robot_fail_2.pkl"
# file_path = "C:\\Users\\USER\\PycharmProjects\\AIing\\save_network_1.pkl"

# Now, you can load the instance back from the file
with open(file_path, "rb") as file:
    loaded_network = pickle.load(file)\

# env.load_simulation(True)
# print(env.run_simulation(loaded_network, False, 1000))
# print(env.run_simulation(loaded_network, False, 1000))
# print(env.run_simulation(loaded_network, False, 1000))
# print(env.run_simulation(loaded_network, False, 1000))
# print(env.run_simulation(loaded_network, False, 1000))
# env.unload_simulation()

env.load_simulation(True)
# print(env.run_simulation(loaded_network, True, 3000, False, True))
print(env.run_simulation(loaded_network, True, 3000))
env.unload_simulation()
