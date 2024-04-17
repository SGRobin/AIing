# Importing Libraries
import pickle

import serial
import time

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

file_path = "..\\networks\\kinda_ok_walk_4.4.pkl"

with open(file_path, "rb") as file:
    loaded_network = pickle.load(file)


# def write_read(x):
#     arduino.write(x)
#     time.sleep(0.05)
#     data = arduino.readline()
#     return data


# while True:
    # num = input("Enter a number: ")  # Taking input from user
input()
    # loaded_network.predict()
arduino.write(bytearray([i for i in range(18)]))
arr = []
arduino.read()
for i in range(18):
    arr.append(int.from_bytes(arduino.read(), "big"))
print(arr)
    # value = write_read(bytearray([i for i in range(18)]))
    # time.sleep(1)
    # print(value)  # printing the value
