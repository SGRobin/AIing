import pickle
import random

from neural_network import NeuralNetwork
from worms import worm_agent

AGENT = worm_agent

POPULATION_SIZE = 11
NUM_OF_POPULATIONS = 4
MAX_GENERATIONS = 2000

MUTATION_RATE = 0.05
STARTING_MUTATION_RANGE = 3.6
MUTATION_RANGE_DOWNWARDS_MULTIPLIER = 0.95
STUCK_GENERATIONS_TO_DECREASE = 10
MUTATION_RANGE_UPWARDS_MULTIPLIER = 1.01
STUCK_GENERATIONS_TO_INCREASE = 100

SAVE_GENERATION = False
PRINT_PROGRESS = True


def parameter_optimization(trial):
    global MUTATION_RATE
    global STARTING_MUTATION_RANGE
    global MUTATION_RANGE_DOWNWARDS_MULTIPLIER
    global STUCK_GENERATIONS_TO_DECREASE
    global MUTATION_RANGE_UPWARDS_MULTIPLIER
    global STUCK_GENERATIONS_TO_INCREASE
    network_size = [trial.suggest_int('layer 1', 32, 64),
                    trial.suggest_int('layer 2', 32, 64),
                    trial.suggest_int('layer 3', 32, 64),
                    trial.suggest_int('layer 4', 32, 64),
                    18]

    MUTATION_RATE = trial.suggest_float('mutation_rate', 0.01, 0.5)
    STARTING_MUTATION_RANGE = trial.suggest_float('mutation_range', 1, 6)
    population = initialize_population(network_size, 18)

    MUTATION_RANGE_DOWNWARDS_MULTIPLIER = trial.suggest_float('mutation_range_downwards_multiplier', 0.9, 1)
    STUCK_GENERATIONS_TO_DECREASE = trial.suggest_int('stuck_generations_to_decrease', 5, 15)
    MUTATION_RANGE_UPWARDS_MULTIPLIER = trial.suggest_float('mutation_range_upwards_multiplier', 1, 1.1)
    STUCK_GENERATIONS_TO_INCREASE = trial.suggest_int('stuck_generations_to_increase', 50, 200)

    population = train_population(population)

    average_fitness = (sum(population[i].fitness_history[0] for i in range(len(population))) / len(population))
    return average_fitness


def initialize_population(network_size, num_of_inputs):
    """
    creates a new population with a population of NeuralNetworks with random weights and biases
    :param num_of_inputs int
    :param network_size: array [], with sizes of each layer
    :return:
    """
    population = []
    for _ in range(POPULATION_SIZE):
        model = NeuralNetwork(network_size, num_of_inputs, MUTATION_RATE, STARTING_MUTATION_RANGE)
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

    # Mutate the whole population:
    next_generation = []
    for i in range(POPULATION_SIZE):
        population[i].fitness_history.insert(0, population[i].fitness_history[0])
        mutating_kid = population[i].clone()
        mutating_kid.mutate()
        next_generation.append(mutating_kid)

    # Calculate the fitness scores of the population:
    fitness_scores = AGENT.evaluate_fitness(next_generation)

    # Replace the ones that the mutation upgraded them:
    for i in range(POPULATION_SIZE):

        # Add correct fitness
        if fitness_scores[i] > population[i].fitness_history[0]:
            # print(f"new: {fitness_scores[i]}, old: {population[i].fitness_history[0]}")
            next_generation[i].fitness_history[0] = fitness_scores[i]  # add fitness
            next_generation[i].generations_stuck = 0
        else:
            next_generation[i] = population[i].clone()
            next_generation[i].generations_stuck += 1

            # Change the mutation range if stuck
            num_stuck = next_generation[i].generations_stuck

            if num_stuck >= STUCK_GENERATIONS_TO_INCREASE and \
                    next_generation[i].mutation_range <= STARTING_MUTATION_RANGE:
                next_generation[i].mutation_range *= MUTATION_RANGE_UPWARDS_MULTIPLIER
            elif num_stuck % STUCK_GENERATIONS_TO_DECREASE == 0 and num_stuck <= STUCK_GENERATIONS_TO_INCREASE:
                next_generation[i].mutation_range *= MUTATION_RANGE_DOWNWARDS_MULTIPLIER

    # print(fitness_scores)
    # fitness_scores_1 = AGENT.evaluate_fitness(next_generation)
    # print(fitness_scores_1)
    # for i in range(len(fitness_scores)):
    #     if fitness_scores_1[i] < fitness_scores[i]:
    #         print("ERROR ERROR ERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR")
    #

    print(
        [
            f"fitness: {next_generation[i].fitness_history[0]}, " +
            f"num stuck: {next_generation[i].generations_stuck}, " +
            f"mutation range: {next_generation[i].mutation_range}" for i in range(POPULATION_SIZE)])
    # f"fitness: {next_generation[i].fitness_history[0]}, " for i in range(POPULATION_SIZE)])
    return next_generation


def train_population(population):
    """
    trains a population over "generation" generations
    :param population: population[NeuralNetwork] - the population that is being trained
    :return: trained_population[NeuralNetwork]
    """
    for generation in range(MAX_GENERATIONS):
        if PRINT_PROGRESS:
            print(f"Generation {generation + 1}:")

        population = train_generation(population)

        # Save it:
        if SAVE_GENERATION:
            save(population[0], f"networks/save_network_generation.pkl")

    # # Show Graph:
    # time_steps = np.arrange(1, len(total_array) + 1)
    # plt.plot(time_steps, np.array(total_array))
    # plt.show()
    return population


def train(agent, network_size, num_of_inputs):
    """
    Trains "num_of_populations" populations and then merges them and trained the best of each together
    :param agent: agent.py - the agent we use
    :param network_size: [x, y] - size of neural network
    :param num_of_inputs: int - number of inputs in the neural network
    :return: NeuralNetwork - the best network
    """
    global AGENT
    AGENT = agent

    best_networks = []
    # Training loop
    for population_num in range(NUM_OF_POPULATIONS):
        if PRINT_PROGRESS:
            print(f"Population number {population_num + 1}:")
        population = initialize_population(network_size, num_of_inputs)

        population = train_population(population)

        # calculate the fitness scores of the population
        fitness_scores = AGENT.evaluate_fitness(population)

        # sort the population by fitness scores
        population = sorted(population, key=lambda obj: fitness_scores[population.index(obj)], reverse=True)

        for i in range(int(POPULATION_SIZE / NUM_OF_POPULATIONS)):
            best_networks.append(population[i])

        save(population[0], f"save_network_{population_num}.pkl")

    trained_best_networks = train_population(best_networks)
    # Get the best-performing network
    best_network = trained_best_networks[0]
    return best_network
