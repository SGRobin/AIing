import pickle

import serial

import Simulation.env_create as env


def walk_robot(arduino, gui):
    file_path = r"C:\Users\shlom\PycharmProjects\AIing\networks\excelente_5.5.pkl"

    with open(file_path, "rb") as file:
        loaded_network = pickle.load(file)

    simulation = env.Simulation(gui)
    simulation.run_arduino_simulation(arduino, loaded_network)
    simulation.unload_simulation()


if __name__ == "__main__":
    try:
        arduino = serial.Serial(port='COM6', baudrate=9600, timeout=2, exclusive=True)
        walk_robot(arduino, True)
    finally:
        arduino.close()

