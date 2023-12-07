import numpy as np

import necessities

# XOR dataset
test_inputs = np.array([np.array([0, 0]), np.array([0, 1]), np.array([1, 0]), np.array([1, 1])])
test_outputs = np.array([0, 1, 1, 0])

# Genetic Algorithm parameters
population_size = 100
generations = 1000
mutation_rate = 0.1
network_size = [2, 1, 1]


# Function to evaluate the fitness of each neural network
def evaluate_fitness(network, test_inputs, test_outputs):
    predictions = []
    for input in test_inputs:
        predictions.append(network.predict(input))
    error = 0
    for i, output in enumerate(test_outputs):
        error += abs(output - predictions[i][0])
    return 1 / (1 + error)


# Genetic Algorithm
population = necessities.initialize_population(population_size, network_size)

# Training loop
for generation in range(generations):
    # Evaluate fitness
    fitness_scores = [evaluate_fitness(network, test_inputs, test_outputs) for network in population]

    top_40_fitness = necessities.get_top_percent_indexes(fitness_scores, 40)

    # Create next generation through crossover and mutation
    next_generation = []
    for i in range(len(top_40_fitness)):
        clone = population[top_40_fitness[i]].clone()
        population[top_40_fitness[i]].mutate(mutation_rate)
        clone.mutate(mutation_rate)
        next_generation.append(population[top_40_fitness[i]])
        next_generation.append(clone)

    top_10_fitness = necessities.get_top_percent_indexes(fitness_scores, 10)
    for i in range(len(top_10_fitness)):
        next_generation.append(population[top_10_fitness[i]])

    top_20_fitness = necessities.get_top_percent_indexes(fitness_scores, 20)
    for i in range(0, len(top_20_fitness), 2):
        next_generation.append(necessities.crossover(population[top_20_fitness[i]], population[top_20_fitness[i + 1]]))

    print(generation)
    population = next_generation

# Get the best-performing network
best_network = max(population, key=lambda network: evaluate_fitness(network, test_inputs, test_outputs))

# Test the best-performing network
predictions = []
for i in range(len(test_inputs)):
    predictions.append(best_network.predict(test_inputs[i]))
print("Predictions:")
print(predictions)
print(test_outputs)
