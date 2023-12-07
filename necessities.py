import random

import numpy as np

from neural_network import NeuralNetwork


def initialize_population(population_size, network_size):
    """
    creates a new population with a population of NeuralNetworks with random weights and biases
    :param population_size: int
    :param network_size: array [], with sizes of each layer
    :return:
    """
    population = []
    for _ in range(population_size):
        model = NeuralNetwork(network_size)
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


# model = NeuralNetwork([2, 3, 1])
#
# weights3 = np.array([np.array([random.random(), random.random(), random.random()])])
#
# weights1 = np.array([np.array([random.random(), random.random()]), np.array([random.random(), random.random()])])
#
# weights2 = np.array([np.array([random.random(), random.random()]),
#                      np.array([random.random(), random.random()]),
#                      np.array([random.random(), random.random()])])
# biases3 = np.array([random.random()])
# biases1 = np.array([random.random(), random.random()])
# biases2 = np.array([random.random(), random.random(), random.random()])
#
# model.set_layer(0, weights1, biases1)
# model.set_layer(1, weights2, biases2)
# model.set_layer(2, weights3, biases3)
#
#
# model1 = NeuralNetwork([2, 3, 1])
#
# weights3 = np.array([np.array([random.random(), random.random(), random.random()])])
#
# weights1 = np.array([np.array([random.random(), random.random()]), np.array([random.random(), random.random()])])
#
# weights2 = np.array([np.array([random.random(), random.random()]),
#                      np.array([random.random(), random.random()]),
#                      np.array([random.random(), random.random()])])
# biases3 = np.array([random.random()])
# biases1 = np.array([random.random(), random.random()])
# biases2 = np.array([random.random(), random.random(), random.random()])
#
# model1.set_layer(0, weights1, biases1)
# model1.set_layer(1, weights2, biases2)
# model1.set_layer(2, weights3, biases3)
#
# model.print_network()
# print(" ")
# model1.print_network()
# print(" ")
# crossover(model, model1).print_network()
