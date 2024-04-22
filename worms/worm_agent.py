

# Function to evaluate the fitness of each neural network
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


def make_warm_worm():
    import ctypes
    dll = ctypes.WinDLL('User32.dll')
    VK_CAPITAL = 0X14
    if not dll.GetKeyState(VK_CAPITAL):
        dll.keybd_event(VK_CAPITAL, 0X3a, 0X1, 0)
        dll.keybd_event(VK_CAPITAL, 0X3a, 0X3, 0)

    return dll.GetKeyState(VK_CAPITAL)


make_warm_worm()
