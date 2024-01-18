import pickle

import necessities
import testing.xor_agent as xor_agent
import robot_agent

import Simulation.env_create as env
from worms import worm_agent

# Genetic Algorithm parameters
agent = worm_agent
# agent = robot_agent
population_size = 50
num_of_populations = 1
max_generations = 5000
mutation_rate = 0.15
mutation_range = 0.5
# network_size = [36, 54, 36, 18]
network_size = [36, 18]
num_of_inputs = 18

# mutation_percentage = 83
crossover_percentage = 0
keep_percentage = 4
mutation_percentage = 100 - crossover_percentage - keep_percentage

check_percentage = 10
print_progress = True
show_simulation = False
save_progress = True

if mutation_percentage + crossover_percentage + keep_percentage != 100:
    raise ValueError("bad percentages")
for percentage in [(mutation_percentage / 2), crossover_percentage, keep_percentage, check_percentage]:
    percentage_pop_size = population_size * (0.01 * percentage)
    if not percentage_pop_size == float(int(percentage_pop_size)):
        raise ValueError("bad percentages")

if agent == robot_agent:
    env.load_simulation(show_simulation)

# Get the best-performing network
best_network = necessities.train(agent=agent,
                                 network_size=network_size,
                                 num_of_inputs=num_of_inputs,
                                 num_of_populations=num_of_populations,
                                 max_generations=max_generations,
                                 population_size=population_size,
                                 mutation_rate=mutation_rate,
                                 mutation_range=mutation_range,
                                 mutation_percentage=mutation_percentage,
                                 crossover_percentage=crossover_percentage,
                                 keep_percentage=keep_percentage,
                                 check_percentage=check_percentage,
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
