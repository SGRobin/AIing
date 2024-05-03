import pickle
import random

import constants
from neural_network import NeuralNetwork
from worms import worm_agent

AGENT = worm_agent


def initialize_population(network_size, num_of_inputs):
    """
    creates a new population with a population of NeuralNetworks with random weights and biases
    :param num_of_inputs int
    :param network_size: array [], with sizes of each layer
    :return:
    """
    population = []

    if constants.USE_EXISTING_NETWORK:
        with open(constants.INITIAL_FILE_PATH, "rb") as file:
            loaded_network = pickle.load(file)
        loaded_network.generations_stuck = 0

        for _ in range(constants.POPULATION_SIZE):
            clone = loaded_network.clone()
            population.append(clone)

    else:
        for _ in range(constants.POPULATION_SIZE):
            model = NeuralNetwork(network_size, num_of_inputs, constants.MUTATION_RATE,
                                  constants.STARTING_MUTATION_RANGE)
            population.append(model)

    fitness_scores = AGENT.evaluate_fitness(population)
    for i in range(constants.POPULATION_SIZE):
        population[i].fitness_history[0] = fitness_scores[i]
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
    midpoint = random.randint(2, len(network_1.get_layer_sizes()) - 2)

    crossed_network = network_2.clone()
    for i in range(midpoint):
        crossed_network.set_layer(i, network_1.get_layer_weights(i), network_1.get_layer_biases(i))

    return crossed_network


def generate_outcast(population):
    """
    creates a new neural network based on the population - either a mutation of a good network or a crossover of networks
    :param population: [NeuralNetwork]
    :return: NeuralNetwork
    """
    if random.random() < 0.3:
        num1 = random.randint(0, 15)
        num2 = num1
        while num2 == num1:
            num2 = random.randint(0, 15)
        return crossover(population[num1], population[num2])
    else:
        extra_network = population[random.randint(0, 10)].clone()
        extra_network.generations_stuck = 0
        extra_network.mutation_range = constants.STARTING_MUTATION_RANGE * 5
        extra_network.mutate()
        extra_network.mutation_range = constants.STARTING_MUTATION_RANGE
        return extra_network


def save(network, path):
    """
    saves the network it gets as a class
    :param path: str "C:something\\another_thing\\"
    :param network: NeuralNetwork
    :return: Nothing
    """
    file_path = path

    with open(file_path, "wb") as file:
        pickle.dump(network, file)


def train_generation(population):
    """
    trains one single generation by using mutation and crossovers
    :param population: population[NeuralNetwork] - the population that is being trained
    :return: trained_population[NeuralNetwork]
    """

    # sort the population by fitness scores:
    population = sorted(population, key=lambda network: network.fitness_history[0], reverse=True)

    # Mutate the whole population except the worst one:
    next_generation = []
    for i in range(constants.POPULATION_SIZE - constants.NUM_REPLACED):

        # Change the mutation range if stuck
        num_stuck = population[i].generations_stuck
        if num_stuck > constants.STUCK_GENERATIONS_TO_SUICIDE and i > 15:
            continue

        if num_stuck >= constants.STUCK_GENERATIONS_TO_INCREASE and \
                population[i].mutation_range <= constants.STARTING_MUTATION_RANGE:
            population[i].mutation_range *= constants.MUTATION_RANGE_UPWARDS_MULTIPLIER
        elif num_stuck % constants.STUCK_GENERATIONS_TO_DECREASE == 0 and num_stuck <= constants.STUCK_GENERATIONS_TO_INCREASE:
            population[i].mutation_range *= constants.MUTATION_RANGE_DOWNWARDS_MULTIPLIER

        population[i].fitness_history.insert(0, population[i].fitness_history[0])
        mutating_kid = population[i].clone()
        mutating_kid.mutate()
        next_generation.append(mutating_kid)

    # fill in the blanks
    num_to_replace = constants.POPULATION_SIZE - len(next_generation)
    for i in range(num_to_replace):
        next_generation.append(generate_outcast(population))

    # Calculate the fitness scores of the population:
    fitness_scores = AGENT.evaluate_fitness(next_generation)

    # Replace the ones that the mutation upgraded them:
    for i in range(constants.POPULATION_SIZE - num_to_replace):

        # Add correct fitness
        if fitness_scores[i] > population[i].fitness_history[0]:
            # print(f"new: {fitness_scores[i]}, old: {population[i].fitness_history[0]}")
            next_generation[i].fitness_history[0] = fitness_scores[i]  # add fitness
            next_generation[i].generations_stuck = 0
        else:
            next_generation[i] = population[i].clone()
            next_generation[i].generations_stuck += 1

    # Set the Harsh clone's fitness
    for i in range(num_to_replace):
        next_generation[constants.POPULATION_SIZE - (i + 1)].fitness_history.insert(0, fitness_scores[
            constants.POPULATION_SIZE - (i + 1)])

    print(
        [
            f"fitness: {next_generation[i].fitness_history[0]}, " for i in range(constants.POPULATION_SIZE)])
    # print(next_generation[0].fitness_history[0])
    return next_generation


def train_population(population):
    """
    trains a population over "generation" generations
    :param population: population[NeuralNetwork] - the population that is being trained
    :return: trained_population[NeuralNetwork]
    """
    for generation in range(constants.MAX_GENERATIONS):
        if constants.PRINT_PROGRESS:
            print(f"Generation {generation + 1}:")

        population = train_generation(population)

        # exit loop:
        if population[0].generations_stuck >= constants.STUCK_GENERATIONS_TO_MOVE_ON:
            return population

        # Save it:
        if constants.SAVE_GENERATION:
            save(population[0], f"networks/save_network_generation.pkl")

    return population


def train(agent, network_size, num_of_inputs):
    """
    Trains "constants.NUM_OF_POPULATIONS" populations and then merges them and trained the best of each together
    :param agent: agent.py - the agent we use
    :param network_size: [x, y] - size of neural network
    :param num_of_inputs: int - number of inputs in the neural network
    :return: NeuralNetwork - the best network
    """
    global AGENT
    AGENT = agent

    best_networks = []
    # Training loop
    for population_num in range(constants.NUM_OF_POPULATIONS):
        if constants.PRINT_PROGRESS:
            print(f"Population number {population_num + 1}:")
        population = initialize_population(network_size, num_of_inputs)

        population = train_population(population)

        # calculate the fitness scores of the population
        fitness_scores = AGENT.evaluate_fitness(population)

        # sort the population by fitness scores
        population = sorted(population, key=lambda obj: fitness_scores[population.index(obj)], reverse=True)

        for i in range(int(constants.POPULATION_SIZE / constants.NUM_OF_POPULATIONS)):
            best_networks.append(population[i])

        save(population[0], f"save_network_{population_num}.pkl")

    trained_best_networks = train_population(best_networks)
    # Get the best-performing network
    best_network = trained_best_networks[0]
    return best_network
