from MultiprocessingSlave import multiprocessing_slave
from worms.worm_engine import create_and_run_simulation


def initialize():
    pass


def evaluate_fitness(networks):
    distances = multiprocessing_slave.executor.map(create_and_run_simulation, networks)
    return [d for d in distances]


def unload_simulations():
    pass


def get_save_path():
    return "networks/worm_network.pkl"
