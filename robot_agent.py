import Simulation.env_create as env
from MultiprocessingSlave import multiprocessing_slave
from constants import NUM_CORPSE

simulation = None


def initialize(show_simulation):
    multiprocessing_slave.executor.map(create_magic_simulation, [show_simulation] * NUM_CORPSE)


def create_magic_simulation(show_simulation):
    global simulation
    simulation = env.Simulation(show_simulation)


def evaluate_fitness(networks):
    distances = multiprocessing_slave.executor.map(run_simulation, networks)
    return [d for d in distances]


def run_simulation(network):
    result = simulation.run_simulation(network)
    return result


def unload_simulation():
    multiprocessing_slave.executor.map(simulation.unload_simulation, [None] * NUM_CORPSE)
