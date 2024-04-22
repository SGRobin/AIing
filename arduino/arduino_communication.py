# Importing Libraries
import pickle

import serial

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

file_path = "..\\networks\\kinda_ok_walk_4.4.pkl"

with open(file_path, "rb") as file:
    loaded_network = pickle.load(file)


def write_read(user_control=True, first_read=False):
    angles = []
    if user_control:
        print("Enter three angles (for three joint types):"
              "example: 23 56 83")

        angles = [int(i) for i in input().split()]

    arduino.write(bytearray([*([angles[0]] * 6), *([angles[1]] * 6), *([angles[2]] * 6)]))
    if first_read:
        arduino.read()
    arr = []
    for i in range(18):
        arr.append(int.from_bytes(arduino.read(), "big"))
    print(arr)


write_read(first_read=True)

while True:
    write_read()
