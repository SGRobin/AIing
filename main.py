import pickle

import necessities
import testing.xor_agent as xor_agent
import robot_agent

import Simulation.env_create as env
# Genetic Algorithm parameters
agent = robot_agent
population_size = 100
num_of_populations = 5
max_generations = 300
mutation_rate = 0.15
mutation_range = 0.5
network_size = [32, 18]
num_of_inputs = 18
mutation_percentage = 84
crossover_percentage = 10
keep_percentage = 6
check_percentage = population_size / num_of_populations
print_progress = True
show_simulation = False

if (mutation_percentage + crossover_percentage + keep_percentage) % population_size != 0:
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
                                 print_progress=print_progress
                                 )


# Test the best-performing network for xor agent
file_path = None
if agent == xor_agent:
    predictions = []
    for i in range(len(xor_agent.test_inputs)):
        predictions.append(best_network.predict(xor_agent.test_inputs[i]))
    print(f"Predictions: {predictions}")
    print(xor_agent.test_outputs)

    file_path = "xor_network.pkl"

if agent == robot_agent:

    file_path = "robot_network.pkl"

# Save the instance to a file
with open(file_path, "wb") as file:
    pickle.dump(best_network, file)

if agent == robot_agent:
    env.unload_simulation()
