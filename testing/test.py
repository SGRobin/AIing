import numpy as np


def python_to_robot_angles(angles):
    # print(outputs)
    # angles = np.degrees((np.array(outputs) * 1.2) - 0.6) + 90
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

arr = []
for i in range(18):
    arr.append(100)
print(arr)
print(python_to_robot_angles(arr))