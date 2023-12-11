import necessities
import testing.xor_agent as xor_agent

# Genetic Algorithm parameters
population_size = 100
num_of_populations = 5
max_generations = 500
mutation_rate = 0.15
mutation_range = 0.5
network_size = [3, 1]
num_of_inputs = 2
mutation_percentage = 84
crossover_percentage = 10
keep_percentage = 6
check_percentage = population_size / num_of_populations
agent = xor_agent
print_progress = True

if population_size % (mutation_percentage + crossover_percentage + keep_percentage) != 0:
    raise ValueError("bad percentages")

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
predictions = []
for i in range(len(xor_agent.test_inputs)):
    predictions.append(best_network.predict(xor_agent.test_inputs[i]))
print(f"Predictions: {predictions}")
print(xor_agent.test_outputs)
