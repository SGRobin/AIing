import numpy as np

from neural_network import NeuralNetwork

# XOR dataset
test_inputs = np.array([np.array([0, 0]), np.array([0, 1]), np.array([1, 0]), np.array([1, 1])])
test_outputs = np.array([0, 1, 1, 0])

# Genetic Algorithm parameters
population_size = 100
generations = 200
mutation_rate = 0.1
network_size = [2, 10, 10, 1]


# Function to initialize a population of neural networks
def initialize_population():
    population = []
    for _ in range(population_size):
        model = NeuralNetwork(network_size)
        population.append(model)
    return population


# Function to evaluate the fitness of each neural network
def evaluate_fitness(network, test_inputs, test_outputs):
    predictions = []
    for input in test_inputs:
        predictions.append(network.predict(input))
    error = 0
    for i, output in enumerate(test_outputs):
        error += abs(output - predictions[i][0])
    return 1 / (1 + error)


def get_top_percent_indexes(arr, percent):
    if not arr:
        return "Array is empty"

    top_percent_count = int(len(arr) * percent / 100)
    sorted_indexes = sorted(range(len(arr)), key=lambda i: arr[i])
    top_percent_indexes = sorted_indexes[-top_percent_count:]

    return top_percent_indexes


# Genetic Algorithm
population = initialize_population()

# Training loop
for generation in range(generations):
    # Evaluate fitness
    fitness_scores = [evaluate_fitness(network, test_inputs, test_outputs) for network in population]

    top_40_fitness = get_top_percent_indexes(fitness_scores, 40)

    # Create next generation through crossover and mutation
    next_generation = []
    for i in range(len(top_40_fitness)):
        clone = population[top_40_fitness[i]].clone()
        population[top_40_fitness[i]].mutate(mutation_rate)
        clone.mutate(mutation_rate)
        next_generation.append(population[top_40_fitness[i]])
        next_generation.append(clone)

    top_20_fitness = get_top_percent_indexes(fitness_scores, 20)
    for i in range(len(top_20_fitness)):
        next_generation.append(population[top_20_fitness[i]])

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
