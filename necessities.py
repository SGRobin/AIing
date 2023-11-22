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
