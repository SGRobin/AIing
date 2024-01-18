

# Function to evaluate the fitness of each neural network
from worms.worm_engine import WormSimulation


def evaluate_fitness(network):
    worm = WormSimulation()
    return worm.run_simulation(network, False)
