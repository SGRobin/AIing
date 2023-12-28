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


def get_top_percent_indexes(arr, percent):
    """
    gets an array and a percentage and returns the indexes of the x% highest numbers
    :param arr: array []
    :param percent: int
    :return: indexes of highest numbers []
    """""
    if not arr:
        raise ValueError("Array is empty")

    top_percent_count = int(len(arr) * percent / 100)
    sorted_indexes = sorted(range(len(arr)), key=lambda i: arr[i])
    top_percent_indexes = sorted_indexes[-top_percent_count:]

    return top_percent_indexes


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
    fitness_scores = [agent.evaluate_fitness(network) for network in population]

    top_mutation_fitness_indexes = get_top_percent_indexes(fitness_scores, mutation_percentage / 2)

    # Create next generation through crossover and mutation
    next_generation = []
    for i in range(len(top_mutation_fitness_indexes)):
        clone = population[top_mutation_fitness_indexes[i]].clone()
        population[top_mutation_fitness_indexes[i]].mutate(mutation_rate, mutation_range)
        clone.mutate(mutation_rate, mutation_range)
        next_generation.append(population[top_mutation_fitness_indexes[i]])
        next_generation.append(clone)

    top_crossover_fitness_indexes = get_top_percent_indexes(fitness_scores, crossover_percentage * 2)
    for i in range(0, len(top_crossover_fitness_indexes), 2):
        next_generation.append(
            crossover(population[top_crossover_fitness_indexes[i]], population[top_crossover_fitness_indexes[i]]))

    top_keep_fitness_indexes = get_top_percent_indexes(fitness_scores, keep_percentage)
    for i in range(len(top_keep_fitness_indexes)):
        next_generation.append(population[top_keep_fitness_indexes[i]])

    top_check_fitness_indexes = get_top_percent_indexes(fitness_scores, check_percentage)
    average_fitness = sum([fitness_scores[i] for i in top_check_fitness_indexes]) / len(
        [fitness_scores[i] for i in top_check_fitness_indexes])

    return next_generation, average_fitness


def train_population(agent, max_generations, population, mutation_rate, mutation_range, mutation_percentage,
                     crossover_percentage, keep_percentage, check_percentage, print_progress=True):
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

    average_fitness_array = []
    for i in range(int(check_percentage / (100 / len(population)))):
        average_fitness_array.append(i)
    generation_checksum = 0
    for generation in range(max_generations):
        population, average_fitness = train_generation(agent, population, mutation_rate, mutation_range,
                                                       mutation_percentage, crossover_percentage, keep_percentage,
                                                       check_percentage)

        average_fitness_array.pop()
        average_fitness_array.insert(0, average_fitness)
        if max(average_fitness_array) - min(
                average_fitness_array) <= min(average_fitness_array) / 10000000000:
            generation_checksum += 1
            if generation_checksum >= check_percentage:
                break
        else:
            generation_checksum = 0

        if print_progress:
            print(f"Generation {generation + 1}")
    return population


def train(agent, network_size, num_of_inputs, num_of_populations, max_generations, population_size, mutation_rate,
          mutation_range, mutation_percentage,
          crossover_percentage, keep_percentage, check_percentage, print_progress):
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
    :return: NeuralNetwork - the best network
    """
    best_networks = []
    # Training loop
    for population_num in range(num_of_populations):
        population = initialize_population(population_size, network_size, num_of_inputs)

        trained_population = train_population(agent, max_generations, population, mutation_rate, mutation_range,
                                              mutation_percentage, crossover_percentage, keep_percentage,
                                              check_percentage, print_progress)
        fitness_scores = [agent.evaluate_fitness(network) for network in trained_population]
        top_population_fitness = get_top_percent_indexes(fitness_scores, int(population_size / num_of_populations))
        if print_progress:
            print(f"Population number: {population_num + 1}")
        for i in range(int(population_size / num_of_populations )):
            best_networks.append(trained_population[top_population_fitness[i]])

    trained_best_networks = train_population(agent, max_generations, best_networks, mutation_rate, mutation_range,
                                             mutation_percentage, crossover_percentage, keep_percentage,
                                             check_percentage, print_progress)
    # Get the best-performing network
    best_network = max(trained_best_networks, key=lambda network: agent.evaluate_fitness(network))
    return best_network
