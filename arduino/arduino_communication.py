# Importing Libraries
import pickle

import numpy as np
import serial

# arduino_angles = [90] * 6 + [100] * 6 + [70] * 6
arduino_angles = [90] * 18

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

file_path = "..\\networks\\kinda_ok_walk_4.4.pkl"

with open(file_path, "rb") as file:
    loaded_network = pickle.load(file)


def python_to_robot_angles(outputs):
    # print(outputs)
    angles = np.degrees((np.array(outputs) * 1.2) - 0.6) + 90
    leg_1 = [angles[15], 180 - angles[16], angles[17]]
    leg_2 = [angles[12], 180 - angles[13], angles[14]]
    leg_3 = [angles[9], 180 - angles[10], angles[11]]
    leg_4 = [angles[0], 180 - angles[1], angles[2]]
    leg_5 = [angles[3], 180 - angles[4], angles[5]]
    leg_6 = [angles[6], 180 - angles[7], angles[8]]
    robot_angles = [leg_1[0], leg_2[0], leg_3[0], leg_4[0], leg_5[0], leg_6[0],
                    leg_1[1], leg_2[1], leg_3[1], leg_4[1], leg_5[1], leg_6[1],
                    leg_1[2], leg_2[2], leg_3[2], leg_4[2], leg_5[2], leg_6[2]]

    return [int(a) for a in robot_angles]


def robot_to_python_angles(angles):
    leg_1 = [angles[0], 180 - angles[6], angles[12]]
    leg_2 = [angles[1], 180 - angles[7], angles[13]]
    leg_3 = [angles[2], 180 - angles[8], angles[14]]
    leg_4 = [angles[3], 180 - angles[9], angles[15]]
    leg_5 = [angles[4], 180 - angles[10], angles[16]]
    leg_6 = [angles[5], 180 - angles[11], angles[17]]
    inputs = np.radians(np.array(leg_4 + leg_5 + leg_6 + leg_3 + leg_2 + leg_1) - 90) * 20 / 3
    # inputs = np.radians(np.array(angles) - 90) * 20 / 3
    print(inputs)
    return inputs


def write_read(user_control=False, first_read=False):
    global arduino_angles
    angles = []
    if user_control:
        print("Enter three angles (for three joint types):"
              "example: 23 56 83")

        angles = [int(i) for i in input().split()]
    else:
        angles = python_to_robot_angles(loaded_network.predict(np.array(robot_to_python_angles(arduino_angles))))

    arduino.write(bytearray([*([angles[0]] * 6), *([angles[1]] * 6), *([angles[2]] * 6)]))
    if first_read:
        arduino.read()
    arduino_angles = []
    for i in range(18):
        arduino_angles.append(int.from_bytes(arduino.read(), "big"))
    # print(arduino_angles)
    # arduino_angles=angles


write_read(first_read=True)

while True:
    write_read()
