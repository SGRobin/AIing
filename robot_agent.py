import Simulation.env_create as env


# Function to evaluate the fitness of each neural network
def evaluate_fitness(network):
    distance = env.run_simulation(network)
    print(distance)
    return distance

