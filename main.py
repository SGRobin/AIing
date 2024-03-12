import concurrent.futures
import pickle

import optuna

import necessities
import robot_agent
import testing.xor_agent as xor_agent
from MultiprocessingSlave import multiprocessing_slave
from constants import NUM_PROCESSES
from worms import worm_agent

# Genetic Algorithm parameters
# AGENT = worm_agent
AGENT = robot_agent
# AGENT = xor_agent

if AGENT == xor_agent:
    network_size = [2, 1]
    num_of_inputs = 2
else:
    network_size = [55, 38, 35, 18]
    num_of_inputs = 18

print_progress = True
save_progress = True


def main():
    with concurrent.futures.ProcessPoolExecutor(max_workers=NUM_PROCESSES) as executor:
        multiprocessing_slave.executor = executor
        AGENT.initialize()

        study = optuna.create_study(direction='maximize')
        study.optimize(necessities.parameter_optimization, n_trials=60)

        print(study.best_value)
        print(study.best_params)

        with open('values_and_parameters_2.txt', 'w') as f:
            f.write(f"value: {study.best_value}.\n" + f"parameters: {study.best_params}")
        # best_network = necessities.train(agent=AGENT,
        #                                  network_size=network_size,
        #                                  num_of_inputs=num_of_inputs,
        #                                  )

    # file_path = AGENT.get_save_path()
    #
    # # Save the instance to a file
    # if save_progress:
    #     with open(file_path, "wb") as file:
    #         pickle.dump(best_network, file)

    # AGENT.unload_simulation()


if __name__ == '__main__':
    main()
