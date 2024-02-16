import concurrent.futures
import pickle

import necessities
import robot_agent
import testing.xor_agent as xor_agent
from MultiprocessingSlave import multiprocessing_slave
from constants import NUM_PROCESSES
from worms import worm_agent

# Genetic Algorithm parameters
agent = worm_agent
# agent = robot_agent
# agent = xor_agent

if agent == xor_agent:
    network_size = [2, 1]
    num_of_inputs = 2
else:
    network_size = [32, 32, 18]
    num_of_inputs = 18

print_progress = True
save_progress = True


def main():
    with concurrent.futures.ProcessPoolExecutor(max_workers=NUM_PROCESSES) as executor:
        multiprocessing_slave.executor = executor
        agent.initialize()

        best_network = necessities.train(agent=agent,
                                         network_size=network_size,
                                         num_of_inputs=num_of_inputs,
                                         print_progress=print_progress,
                                         save_progress=save_progress)

    file_path = None
    # Test the best-performing network for xor agent    file_path = None
    if agent == xor_agent:
        predictions = [] #TODO change
        for i in range(len(xor_agent.test_inputs)):
            predictions.append(best_network.predict(xor_agent.test_inputs[i]))
        print(f"Predictions: {predictions}")
        print(xor_agent.test_outputs)

    file_path = agent.get_save_path()

    # Save the instance to a file

    if save_progress:
        with open(file_path, "wb") as file:
            pickle.dump(best_network, file)

    # agent.unload_simulation()


if __name__ == '__main__':
    main()
