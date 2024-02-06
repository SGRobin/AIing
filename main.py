import pickle

import necessities
import testing.xor_agent as xor_agent
import robot_agent

import Simulation.env_create as env
from worms import worm_agent

# Genetic Algorithm parameters
# agent = worm_agent
agent = robot_agent
# agent =xor_agent

network_size = [32, 32, 32, 18]
# network_size = [2, 1]
num_of_inputs = 18


print_progress = True
show_simulation = False
save_progress = True

if agent == robot_agent:
    env.load_simulation(show_simulation)

# Get the best-performing network
best_network = necessities.train(agent=agent,
                                 network_size=network_size,
                                 num_of_inputs=num_of_inputs,
                                 print_progress=print_progress,
                                 save_progress=save_progress)

# Test the best-performing network for xor agent
file_path = None
if agent == xor_agent:
    predictions = []
    for i in range(len(xor_agent.test_inputs)):
        predictions.append(best_network.predict(xor_agent.test_inputs[i]))
    print(f"Predictions: {predictions}")
    print(xor_agent.test_outputs)

    file_path = "networks/xor_network.pkl"

if agent == robot_agent:

    file_path = "networks/robot_network.pkl"

# Save the instance to a file
if save_progress:
    with open(file_path, "wb") as file:
        pickle.dump(best_network, file)

if agent == robot_agent:
    env.unload_simulation()
