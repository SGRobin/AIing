import pickle
import random

from neural_network import NeuralNetwork

POPULATION_SIZE = 1
NUM_OF_POPULATIONS = 4
MAX_GENERATIONS = 5000

STARTING_MUTATION_RATE = 0.1
STARTING_MUTATION_RANGE = 1
MUTATION_RANGE_DOWNWARDS_MULTIPLIER = 0.95
STUCK_GENERATIONS_TO_DECREASE = 10
MUTATION_RANGE_UPWARDS_MULTIPLIER = 1.01
STUCK_DECREASES_TO_INCREASE = 40

# CROSSOVER = 3
# KEEP_CHAMPIONS = 1
# NEW_RANDOS = 2
CHECK_PERCENTAGE = 10
MAX_STUCK_GENERATIONS = 10
SAVE_GENERATION = False


def initialize_population(network_size, num_of_inputs):
    """
    creates a new population with a population of NeuralNetworks with random weights and biases
    :param num_of_inputs int
    :param network_size: array [], with sizes of each layer
    :return:
    """
    population = []
    for _ in range(POPULATION_SIZE):
        model = NeuralNetwork(network_size, num_of_inputs, STARTING_MUTATION_RATE, STARTING_MUTATION_RANGE)
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
    midpoint = random.randint(1, len(network_1.get_layer_sizes()) - 1)

    crossed_network = network_2.clone()
    for i in range(midpoint):
        crossed_network.set_layer(i, network_1.get_layer_weights(i), network_1.get_layer_biases(i))

    return crossed_network


def save(best_network, path):
    """
    saves the network it gets as a class
    :param path: str "C:something\\another_thing\\"
    :param best_network: NeuralNetwork
    :return: Nothing
    """
    file_path = path

    with open(file_path, "wb") as file:
        pickle.dump(best_network, file)


def train_generation(agent, population):
    """
    trains one single generation by using mutation and crossovers
    :param agent: agent.py - the agent we use
    :param population: population[NeuralNetwork] - the population that is being trained
    :return: trained_population[NeuralNetwork]
    """

    # sort the population by fitness scores:
    population = sorted(population, key=lambda network: network.fitness_history[0], reverse=True)

    # Mutate the whole population:
    next_generation = []
    for i in range(POPULATION_SIZE):
        population[i].fitness_history.insert(0, population[i].fitness_history[0])
        mutating_kid = population[i].clone()
        mutating_kid.mutate()
        next_generation.append(mutating_kid)

    # Calculate the fitness scores of the population:
    fitness_scores = agent.evaluate_fitness(next_generation)

    # Replace the ones that the mutation upgraded them:
    for i in range(POPULATION_SIZE):

        # Add correct fitness
        if fitness_scores[i] > population[i].fitness_history[0]:
            # print(f"new: {fitness_scores[i]}, old: {population[i].fitness_history[0]}")
            next_generation[i].fitness_history.insert(0, fitness_scores[i])  # add fitness
            next_generation[i].generations_stuck = 0
        else:
            next_generation[i].generations_stuck += 1

            # Change the mutation range if stuck
            num_stuck = next_generation[i].generations_stuck
            if num_stuck >= (STUCK_GENERATIONS_TO_DECREASE * STUCK_DECREASES_TO_INCREASE) and\
                    next_generation[i].mutation_range < STARTING_MUTATION_RANGE:
                next_generation[i].mutation_range *= MUTATION_RANGE_UPWARDS_MULTIPLIER
            elif num_stuck % STUCK_GENERATIONS_TO_DECREASE == 0:
                next_generation[i].mutation_range *= MUTATION_RANGE_DOWNWARDS_MULTIPLIER

    print(
        [
            f"fitness: {next_generation[i].fitness_history[0]}, " +
            f"num stuck: {next_generation[i].generations_stuck}, " +
            f"mutation range: {next_generation[i].mutation_range}" for i in range(POPULATION_SIZE)])

    return next_generation


def train_population(agent, population, print_progress=True):
    """
    trains a population over "generation" generations
    :param agent: agent.py - the agent we use
    :param population: population[NeuralNetwork] - the population that is being trained
    :param print_progress Boolean - prints the progress
    :return: trained_population[NeuralNetwork]
    """
    for generation in range(MAX_GENERATIONS):
        if print_progress:
            print(f"Generation {generation + 1}:")

        population = train_generation(agent, population)

        # fitness_array.pop()
        # fitness_array.insert(0, population[0])
        # if fitness_array[0] == fitness_array[1]:
        #     num_stuck_generations += 1
        # else:
        #     num_stuck_generations = 0

        # if num_stuck_generations >= MAX_STUCK_GENERATIONS: #TODO check if it helps
        #     STARTING_MUTATION_RANGE = STARTING_MUTATION_RANGE + np.log10(num_stuck_generations / 10)
        # else:
        #     STARTING_MUTATION_RANGE = STARTING_MUTATION_RANGE

        # if num_stuck_generations >= MAX_STUCK_GENERATIONS * 5:
        #     break

        # Save it:
        if SAVE_GENERATION:
            save(population[0], f"networks/save_network_generation.pkl")

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

        population = train_population(agent, population, print_progress=print_progress)

        # calculate the fitness scores of the population
        fitness_scores = agent.evaluate_fitness(population)

        # sort the population by fitness scores
        population = sorted(population, key=lambda obj: fitness_scores[population.index(obj)], reverse=True)

        for i in range(int(POPULATION_SIZE / NUM_OF_POPULATIONS)):
            best_networks.append(population[i])

        if save_progress:
            save(population[0], f"save_network_{population_num}.pkl")

    trained_best_networks = train_population(agent, best_networks, network_size)
    # Get the best-performing network
    best_network = trained_best_networks[0]
    return best_network
