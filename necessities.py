import pickle

import numpy as np
from matplotlib import pyplot as plt

from constants import MAX_STUCK_GENERATIONS
from neural_network import NeuralNetwork


def initialize_population(population_size, network_size, num_of_inputs):
    """
    creates a new population with a population of NeuralNetworks with random weights and biases
    :param num_of_inputs int
    :param population_size: int
    :param network_size: array [], with sizes of each layer
    :return:
    """
    population = []
    for _ in range(population_size):
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


def train_generation(agent, population, mutation_rate, mutation_range, mutation_percentage, crossover_percentage,
                     keep_percentage, check_percentage):
    """
    trains one single generation by using mutation and crossovers
    :param agent: agent.py - the agent we use
    :param population: population[NeuralNetwork] - the population that is being trained
    :param mutation_rate: int - the rate of mutation
    :param mutation_range: int - the range of mutation
    :param mutation_percentage: int - mutation percentage
    :param crossover_percentage: int - crossover percentage
    :param keep_percentage: int - percentage we keep as is
    :param check_percentage: int - percentage that we check if it's time to stop generations
    :return: trained_population[NeuralNetwork]
    """
    # calculate the fitness scores of the population
    fitness_scores = [agent.evaluate_fitness(network) for network in population]

    # sort the population by fitness scores
    population = sorted(population, key=lambda obj: fitness_scores[population.index(obj)], reverse=True)

    # create next generation and append all the mutations, crossovers and top networks of this population
    next_generation = []
    for i in range(int(((len(population) * mutation_percentage) / 2) / 100)):
        for _ in range(2):
            mutated_kid = population[i].clone()
            mutated_kid.mutate(mutation_rate, mutation_range)
            next_generation.append(mutated_kid)

    for i in range(int((len(population) * crossover_percentage) / 100)):
        next_generation.append(crossover(population[i], population[i]))

    for i in range(int((len(population) * keep_percentage) / 100)):
        next_generation.append(population[i].clone())

    # print(f"size of population is: {len(population)}")
    # get the average fitness of the top check_percentage% to see if it's time to stop training
    average_top_fitness = sum(
        sorted(fitness_scores, reverse=True)[:int(len(fitness_scores) * (check_percentage / 100))]) / int(
        len(fitness_scores) * (check_percentage / 100))

    # Print Top
    array = []
    for score in sorted(fitness_scores, reverse=True)[:10]:
        array.append(score)
    print(array)

    return next_generation, average_top_fitness


def train_population(agent, max_generations, population, mutation_rate, mutation_range, mutation_percentage,
                     crossover_percentage, keep_percentage, check_percentage, print_progress=True, save_progress=False):
    """
    trains a population over "generation" generations
    :param agent: agent.py - the agent we use
    :param max_generations the number of maximum generations
    :param population: population[NeuralNetwork] - the population that is being trained
    :param mutation_rate: int - the rate of mutation
    :param mutation_range: int - the range of mutation
    :param mutation_percentage: int - mutation percentage
    :param crossover_percentage: int - crossover percentage
    :param keep_percentage: int - percentage we keep as is
    :param check_percentage: int - percentage that we check if it's time to stop generations
    :param print_progress Boolean - prints the progress
    :return: trained_population[NeuralNetwork]
    """
    total_array = []
    average_fitness_array = []
    for i in range(int(check_percentage / (100 / len(population)))):
        average_fitness_array.append(i)
    num_stuck_generations = 0

    for generation in range(max_generations):
        if print_progress:
            print(f"Generation {generation + 1} mutation range {mutation_range}")

        population, average_fitness = train_generation(agent, population, mutation_rate, mutation_range,
                                                       mutation_percentage, crossover_percentage, keep_percentage,
                                                       check_percentage)

        average_fitness_array.pop()
        average_fitness_array.insert(0, average_fitness)
        total_array.append(average_fitness)
        if max(average_fitness_array) - min(
                average_fitness_array) <= min(average_fitness_array) / 100000:
            num_stuck_generations += 1
        else:
            num_stuck_generations = 0

        if num_stuck_generations >= MAX_STUCK_GENERATIONS:
            # mutation_range = 2 * base_mutation_range
            # mutation_rate = 2 * base_mutation_rate
            mutation_range *= 1.4
            if mutation_range > 0.5:
                mutation_range = 0.01
        else:
            mutation_range *= 0.9

        if num_stuck_generations >= MAX_STUCK_GENERATIONS * 5:
            break

        # else:
        #     mutation_range = base_mutation_range
        #     mutation_rate = base_mutation_rate
        #     num_stuck_generations = 0

        # Save it:
        save(population[0])

    # # Show Graph:
    # time_steps = np.arange(1, len(total_array) + 1)
    # plt.plot(time_steps, np.array(total_array))
    # plt.show()
    return population


def save(best_network):
    file_path = f"networks/save_worm_network_generation.pkl"

    with open(file_path, "wb") as file:
        pickle.dump(best_network, file)


def train(agent, network_size, num_of_inputs, num_of_populations, max_generations, population_size, mutation_rate,
          mutation_range, mutation_percentage,
          crossover_percentage, keep_percentage, check_percentage, print_progress, save_progress=False):
    """
    traines "num_of_populations" populations and then merges them and trained the best of each together
    :param agent: agent.py - the agent we use
    :param network_size: [x, y] - size of neural network
    :param num_of_inputs: int - number of inputs in the neural network
    :param num_of_populations: int - number of populations we train and then merge
    :param max_generations: int - number of maximum generations each population trains
    :param population_size: int - size of each population
    :param mutation_rate: int - the rate of mutation
    :param mutation_range: int - the range of mutation
    :param mutation_percentage: int - mutation percentage
    :param crossover_percentage: int - crossover percentage
    :param keep_percentage: int - percentage we keep as is
    :param check_percentage: int - percentage that we check if it's time to stop generations
    :param print_progress Boolean - prints the progress
    :param save_progress: Boolean - do you save during runs
    :return: NeuralNetwork - the best network
    """
    best_networks = []
    # Training loop
    for population_num in range(num_of_populations):
        if print_progress:
            print(f"Population number {population_num + 1}:")
        population = initialize_population(population_size, network_size, num_of_inputs)

        trained_population = train_population(agent, max_generations, population, mutation_rate, mutation_range,
                                              mutation_percentage, crossover_percentage, keep_percentage,
                                              check_percentage, print_progress, save_progress)

        # calculate the fitness scores of the population
        fitness_scores = [agent.evaluate_fitness(network) for network in population]

        # sort the population by fitness scores
        population = sorted(population, key=lambda obj: fitness_scores[population.index(obj)], reverse=True)

        for i in range(int(population_size / num_of_populations)):
            best_networks.append(trained_population[i])

        if save_progress:
            file_path = f"save_network_{population_num}.pkl"
            print(file_path)
            best_network = max(trained_population, key=lambda network: agent.evaluate_fitness(network))
            with open(file_path, "wb") as file:
                pickle.dump(best_network, file)

    trained_best_networks = train_population(agent, max_generations, best_networks, mutation_rate, mutation_range,
                                             mutation_percentage, crossover_percentage, keep_percentage,
                                             check_percentage, print_progress)
    # Get the best-performing network
    best_network = max(trained_best_networks, key=lambda network: agent.evaluate_fitness(network))
    return best_network
