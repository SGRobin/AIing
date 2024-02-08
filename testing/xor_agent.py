import numpy as np
# import cupy as np

# XOR dataset
test_inputs = np.array([np.array([0, 0]), np.array([0, 1]), np.array([1, 0]), np.array([1, 1])])
test_outputs = np.array([0, 1, 1, 0])


# Function to evaluate the fitness of each neural network
def evaluate_fitness(networks):
    return [evaluate_single_network(network) for network in networks]


def evaluate_single_network(network):
    predictions = []
    for network_input in test_inputs:
        predictions.append(network.predict(network_input))
    error = 0
    for i, output in enumerate(test_outputs):
        error += (output - predictions[i][0]) ** 2
    return 1 / (1 + error)


def initialize(show_simulation):
    pass


def unload_simulations():
    pass
