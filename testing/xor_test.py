import random

import numpy as np

from neural_network import NeuralNetwork

# XOR dataset
test_inputs = np.array([np.array([0, 0]), np.array([0, 1]), np.array([1, 0]), np.array([1, 1])])
test_outputs = np.array([0, 1, 1, 0])

# Genetic Algorithm parameters
population_size = 100
generations = 1000
mutation_rate = 0.1


# Function to initialize a population of neural networks
def initialize_population():
    population = []
    for _ in range(population_size):
        model = NeuralNetwork([2, 10, 10, 1])
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


# Function for genetic mutation
def mutate(network, mutation_rate):
    mutated_network = NeuralNetwork([2, 10, 10, 1])
    for layer in range(network.get_num_layers()):
        current_biases = network.get_layer_biases(layer)
        mutated_biases = []
        for i in range(len(current_biases)):
            if random.random() < mutation_rate:
                current_biases[i] += random.uniform(-1, 1) * 0.5
            mutated_biases.append(current_biases[i])

        current_weights = network.get_layer_weights(layer)
        # print(current_weights)
        mutated_weights = []
        for weights in current_weights:
            temp_mutated_weights = []
            for i in range(len(weights)):
                if random.random() < mutation_rate:
                    weights[i] += random.uniform(-1, 1)
                temp_mutated_weights.append(weights[i])
            mutated_weights.append(temp_mutated_weights)
        mutated_network.set_layer(layer, weights=np.array(mutated_weights), biases=np.array(mutated_biases))
    return mutated_network


def get_top_50_percent_indexes(arr):
    if not arr:
        return "Array is empty"

    # Calculate the number of elements in the top 50%
    top_50_percent_count = int(len(arr) * 0.5)

    # Use sorted to get the indices of the sorted array
    sorted_indexes = sorted(range(len(arr)), key=lambda i: arr[i])

    # Get the indexes of the top 50% largest numbers
    top_50_percent_indexes = sorted_indexes[-top_50_percent_count:]

    return top_50_percent_indexes


# Genetic Algorithm
population = initialize_population()

# Training loop
for generation in range(generations):
    # Evaluate fitness
    fitness_scores = [evaluate_fitness(network, test_inputs, test_outputs) for network in population]

    top_fitness = get_top_50_percent_indexes(fitness_scores)

    # Create next generation through crossover and mutation
    next_generation = []
    for i in range(population_size // 2):
        mutation_1 = mutate(population[top_fitness[i]], mutation_rate)
        mutation_2 = mutate(population[top_fitness[i]], mutation_rate)
        next_generation.append(mutation_1)
        next_generation.append(mutation_2)


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
