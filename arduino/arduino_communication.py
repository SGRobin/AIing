# Importing Libraries
import pickle
import Simulation.env_create as env
import numpy as np
import serial

# arduino_angles = [90] * 6 + [100] * 6 + [70] * 6

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

file_path = "..\\networks\\kinda_ok_walk_4.4.pkl"

with open(file_path, "rb") as file:
    loaded_network = pickle.load(file)


simulation = env.Simulation(True)
simulation.run_arduino_simulation(arduino, loaded_network)
simulation.unload_simulation()
