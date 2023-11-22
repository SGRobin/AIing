import random

import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class Neuron:
    """
    class that creates a single Neuron
    has all the weights coming into the neuron

    """

    def __init__(self, num_of_weights):
        self.weights = np.array([random.random() for _ in range(num_of_weights)])
        self.bias = random.random()

    def fire(self, inputs):
        """
        function that gets all the inputs and calculates the output of the neuron
        w0 * x1 + w1 * x2 + ... + b
        :param inputs: the input values *numpy array (outputs from last layer)
        :return: outputs
        """
        if len(inputs) != len(self.weights):
            raise ValueError("input and weights sizes don't match")
        return sigmoid(sum(inputs * self.weights) + self.bias)

    def mutate_neuron(self, mutation_rate):
        """
        mutates the Neuron
        :param mutation_rate: 0 < float < 1
        :return:
        """
        new_weights = []
        for weight in self.weights:
            if random.random() < mutation_rate:
                weight += random.gauss(0, 1)
            new_weights.append(weight)
        self.set_weights(np.array(new_weights))

        if random.random() < mutation_rate:
            self.set_bias(self.bias + random.gauss(0, 1))

    def set_weights(self, weights):
        """
        sets the weights
        :param weights: np array of weights
        :return: nothing
        """
        self.weights = weights

    def set_bias(self, bias):
        """
        sets the bias
        :param bias: bias number
        :return: nothing
        """
        self.bias = bias

    def get_weights(self):
        """
        gets the weights
        :return: np.array() of weights
        """
        return self.weights

    def get_bias(self):
        """
        gets the bias
        :return: bias - int
        """
        return self.bias


class Layer:
    """
    class that creates a single Layer

    """

    def __init__(self, size, last_layer_size):
        self.neurons = np.array(list(Neuron(last_layer_size) for _ in range(size)))

    def set_values(self, weights=None, biases=None):
        """
        sets the weights and biases of all the neurons in the layer
        :param weights: np.array() of np.arrays() of weights
        :param biases: np.array() of biases
        :return: nothing
        """
        if weights is not None:
            for i, neuron in enumerate(self.neurons):
                neuron.set_weights(weights[i])
        if biases is not None:
            for i, neuron in enumerate(self.neurons):
                neuron.set_bias(biases[i])

    def mutate_layer(self, mutation_rate):
        """
        mutates a Layer
        :param mutation_rate: 0 < float < 1
        :return:
        """
        for neuron in self.neurons:
            neuron.mutate_neuron(mutation_rate)

    def get_neuron_weights(self):
        """
        gets the weights of all the neurons in the layer
        :return: np.array() of np.arrays() of weights,
        """
        weights = []
        for neuron in self.neurons:
            weights.append(neuron.get_weights())
        return np.array(weights)

    def get_neuron_biases(self):
        """
        gets the biases of all the neurons in the layer
        :return: np.array() of biases
        """
        biases = []
        for neuron in self.neurons:
            biases.append(neuron.get_bias())
        return np.array(biases)


class NeuralNetwork:
    """
    class the creates a Neural Network
    the initiator gets the size of all the layers [input size, hidden size, hidden size, output size]
    """

    def __init__(self, layer_sizes):
        # Create the Layers
        self.layer_sizes = layer_sizes
        self.layers = [Layer(layer_sizes[0], layer_sizes[0])]
        for i in range(1, len(layer_sizes)):
            self.layers.append(Layer(layer_sizes[i], layer_sizes[i - 1]))

    def predict(self, inputs):
        """
        gets inputs for the Neural Network and gives an output
        :param inputs: input values *numpy array
        :return: outputs of the Neural Network
        """
        for layer in self.layers:
            inputs = np.array([neuron.fire(inputs) for neuron in layer.neurons])
        return inputs

    def mutate(self, mutation_rate):
        """
        mutates the Network
        :param mutation_rate: 0 < float < 1
        :return:
        """
        for layer in self.layers:
            layer.mutate_layer(mutation_rate)

    def clone(self):
        """
        clones the Network
        :return: NeuralNetwork
        """
        cloned_network = NeuralNetwork(self.layer_sizes)
        for i in range(len(self.layers)):
            cloned_network.set_layer(i, self.get_layer_weights(i), self.get_layer_biases(i))

        return cloned_network

    def set_layer(self, layer_index, weights=None, biases=None):
        """
        sets the weights and biases of all the neurons in a single layer
        :param layer_index: the layer that the function changes - int
        :param weights: np.array() of np.arrays() of weights
        :param biases: np.array() of biases
        :return: nothing
        """
        if len(self.layers) < layer_index:
            raise ValueError("layer index larger than num of layers")
        self.layers[layer_index].set_values(weights, biases)

    def get_num_layers(self):
        """
        returns number of layers
        :return: int
        """
        return len(self.layers)

    def get_layer_weights(self, layer_index):
        """
        gets the weights of all the neurons in a layer
        :return: np.array() of np.arrays() of weights,
        """
        return self.layers[layer_index].get_neuron_weights()

    def get_layer_biases(self, layer_index):
        """
        gets the biases of all the neurons in a layer
        :return: np.array() of biases
        """
        return self.layers[layer_index].get_neuron_biases()

    def print_network(self, inputs):
        """
        gets inputs for the Neural Network and prints it to see
        :param inputs: input values *numpy array
        """
        for layer in self.layers:
            outputs = np.array([])
            for neuron in layer.neurons:
                outputs = np.append(outputs, neuron.fire(inputs))
            inputs = outputs
            print(outputs)

# model = NeuralNetwork([2, 3, 1])

# weights1 = np.array([random.np.array([random()])])
# weights2 = np.array([random.np.array([random.random(), random()]), random.np.array([random.random(), random()])])
# weights3 = np.array([random.np.array([random.random(), random.random(), random()]), random.np.array([random.random(), random.random(), random()]), random.np.array([random.random(), random.random(), random()])])
# biases1 = random.np.array([random()])
# biases2 = random.np.array([random.random(), random()])
# biases3 = random.np.array([random.random(), random.random(), random()])
#
# model.set_layer(0, weights2, biases2)
# model.set_layer(1, weights3, biases3)
# model.set_layer(2, weights1, biases1)

# model.print_network(np.array([1, 2]))
# print(np.array([1, 2]))
# model.predict(np.array([0, 0]))
# current_weights = model.get_layer_weights(0)
# mutated_weights = np.array([])
# print(current_weights)
