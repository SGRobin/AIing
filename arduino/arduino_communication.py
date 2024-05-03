import pickle

import serial

import Simulation.env_create as env

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
# arduino = 10

file_path = "..\\networks\\walk_3.5.pkl"

with open(file_path, "rb") as file:
    loaded_network = pickle.load(file)

simulation = env.Simulation(True)
simulation.run_arduino_simulation(arduino, loaded_network)
simulation.unload_simulation()
