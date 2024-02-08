import pickle
import time

import numpy as np

from neural_network import NeuralNetwork

POPULATION_SIZE = 40
NUM_OF_POPULATIONS = 1
MAX_GENERATIONS = 5000
MUTATION_RATE = 0.5
MUTATION_RANGE = 0.5
CROSSOVER = 3
KEEP_CHAMPIONS = 1
NEW_RANDOS = 2
CHECK_PERCENTAGE = 10
MAX_STUCK_GENERATIONS = 10
SAVE_GENERATION = True


def initialize_population(network_size, num_of_inputs):
    """
    creates a new population with a population of NeuralNetworks with random weights and biases
    :param num_of_inputs int
    :param network_size: array [], with sizes of each layer
    :return:
    """
    population = []
    for _ in range(POPULATION_SIZE):
        model = NeuralNetwork(network_size, num_of_inputs)
        population.append(model)
    return population


def crossover(network_1: NeuralNetwork, network_2: NeuralNetwork):
    """
    crosses over 2 networks - combines half the layers of each
    :param network_1: NeuralNetwork
    :param network_2: NeuralNetwork
    :return: NeuralNetwork
    """
    if network_1.get_layer_sizes() != network_2.get_layer_sizes():
        raise ValueError("network not the same size")
    # Calculate the midpoint index
    midpoint = network_2.get_num_layers() // 2

    crossed_network = network_2.clone()
    for i in range(midpoint):
        crossed_network.set_layer(i, network_1.get_layer_weights(i), network_1.get_layer_biases(i))

    return crossed_network


def save(best_network):
    """
    saves the network it gets as a class
    :param best_network: NeuralNetwork
    :return: Nothing
    """
    file_path = f"networks/save_network_generation.pkl"

    with open(file_path, "wb") as file:
        pickle.dump(best_network, file)


def train_generation(agent, population, mutation_range, mutation_rate, network_size, num_of_inputs):
    """
    trains one single generation by using mutation and crossovers
    :param network_size: [x, y] - size of neural network
    :param num_of_inputs: int - number of inputs in the neural network
    :param agent: agent.py - the agent we use
    :param population: population[NeuralNetwork] - the population that is being trained
    :param mutation_rate: int - the rate of mutation
    :param mutation_range: int - the range of mutation
    :return: trained_population[NeuralNetwork]
    """
    # calculate the fitness scores of the population
    start_time = time.time()

    fitness_scores = agent.evaluate_fitness(population)

    # fitness_scores = list(executor.map(agent.evaluate_fitness, population))
    # fitness_scores = []
    # for i in range(len(population)):
    #     fitness_scores += list(executor.map(agent.evaluate_fitness, population[12*i::12+12*i]))

    end_time = time.time()
    print(f"fitness time: {end_time - start_time}")

    # sort the population by fitness scores
    population = sorted(population, key=lambda obj: fitness_scores[population.index(obj)], reverse=True)

    next_generation = [population[0].clone()]

    start_time = time.time()
    for _ in range(len(population) - 1):
        mutated_kid = population[0].clone()
        mutated_kid.mutate(mutation_rate, mutation_range)
        next_generation.append(mutated_kid)
    end_time = time.time()
    print(f"mutation time: {end_time - start_time}")

    # print(f"size of population is: {len(population)}")

    # Print Top
    array = []
    for score in sorted(fitness_scores, reverse=True)[:10]:
        array.append(score)
    print(array)

    return next_generation, array[0]


def train_population(agent, population, network_size, num_of_inputs, print_progress=True):
    """
    trains a population over "generation" generations
    :param network_size: [x, y] - size of neural network
    :param num_of_inputs: int - number of inputs in the neural network
    :param agent: agent.py - the agent we use
    :param population: population[NeuralNetwork] - the population that is being trained
    :param print_progress Boolean - prints the progress
    :return: trained_population[NeuralNetwork]
    """
    fitness_array = [1, 2]
    num_stuck_generations = 0
    mutation_range = MUTATION_RANGE

    for generation in range(MAX_GENERATIONS):
        if print_progress:
            print(f"Generation {generation + 1} mutation range {mutation_range}")

        population, top_fitness = train_generation(agent, population, mutation_range, MUTATION_RATE, network_size,
                                                   num_of_inputs)

        fitness_array.pop()
        fitness_array.insert(0, top_fitness)
        if fitness_array[0] == fitness_array[1]:
            num_stuck_generations += 1
        else:
            num_stuck_generations = 0

        if num_stuck_generations >= MAX_STUCK_GENERATIONS:
            mutation_range = MUTATION_RANGE + np.log10(num_stuck_generations / 10)
        else:
            mutation_range = MUTATION_RANGE

        if num_stuck_generations >= MAX_STUCK_GENERATIONS * 5:
            break

        # Save it:
        if SAVE_GENERATION:
            save(population[0])

    # # Show Graph:
    # time_steps = np.arrange(1, len(total_array) + 1)
    # plt.plot(time_steps, np.array(total_array))
    # plt.show()
    return population


def train(agent, network_size, num_of_inputs, print_progress, save_progress=False):
    """
    Trains "num_of_populations" populations and then merges them and trained the best of each together
    :param agent: agent.py - the agent we use
    :param network_size: [x, y] - size of neural network
    :param num_of_inputs: int - number of inputs in the neural network
    :param print_progress Boolean - prints the progress
    :param save_progress: Boolean - do you save during runs
    :return: NeuralNetwork - the best network
    """
    best_networks = []
    # Training loop
    for population_num in range(NUM_OF_POPULATIONS):
        if print_progress:
            print(f"Population number {population_num + 1}:")
        population = initialize_population(network_size, num_of_inputs)

        trained_population = train_population(agent, population, network_size, num_of_inputs,
                                              print_progress=print_progress)

        # calculate the fitness scores of the population
        fitness_scores = agent.evaluate_fitness(population)

        # sort the population by fitness scores
        population = sorted(population, key=lambda obj: fitness_scores[population.index(obj)], reverse=True)

        for i in range(int(POPULATION_SIZE / NUM_OF_POPULATIONS)):
            best_networks.append(trained_population[i])

        if save_progress:
            file_path = f"save_network_{population_num}.pkl"
            print(file_path)
            best_network = population[0]
            with open(file_path, "wb") as file:
                pickle.dump(best_network, file)

    trained_best_networks = train_population(agent, best_networks, network_size, num_of_inputs, print_progress)
    # Get the best-performing network
    best_network = trained_best_networks[0]
    return best_network
