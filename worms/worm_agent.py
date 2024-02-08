

# Function to evaluate the fitness of each neural network
from MultiprocessingSlave import multiprocessing_slave
from worms.worm_engine import WormSimulation


def initialize(show_simulation):
    pass


def evaluate_fitness(networks):
    worm = WormSimulation()
    distances = multiprocessing_slave.executor.map(worm.run_simulation, networks)
    return [d for d in distances]


def unload_simulations():
    pass
