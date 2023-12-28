import time

# import numpy as np
import cupy as np
import pybullet as p
import pybullet_data

import Simulation.hard_code_walk as hard
import constants

link_ids = [2, 3, 4, 7, 8, 9, 12, 13, 14, 17, 18, 19, 22, 23, 24, 27, 28, 29]
urdf_file_path = "C:\\Users\\USER\\PycharmProjects\\AIing\\Simulation\\models\\crab_model.urdf.xml"
startPos = [0, 0, 0.18]
startOrientation = p.getQuaternionFromEuler([0, 0, 0])
robot_id = None


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def load_simulation(gui=False):
    p.connect(p.GUI if gui else p.DIRECT)  # or p.DIRECT for non-graphical version
    p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
    p.setGravity(0, 0, -9.81)
    p.loadURDF("plane.urdf")
    global robot_id
    robot_id = p.loadURDF(urdf_file_path, startPos, startOrientation)
    for link_id in link_ids:
        p.changeDynamics(robot_id,
                         link_id,
                         lateralFriction=constants.LINEAR_FRICTION,
                         angularDamping=constants.ANGULAR_FRICTION,
                         frictionAnchor=1)


def unload_simulation():
    p.disconnect()


def reset_joints():
    for joint in link_ids:
        p.resetJointState(robot_id, joint, 0)


def run_simulation(network=None, wait=False, time_to_run=2000, network_controlled=True, hard_walk=False):
    reset_joints()
    directions = [0] * 18
    if hard_walk is True:
        for i in range(time_to_run):
            hard.step(robot_id, i)
            p.stepSimulation()

    if network_controlled is True:
        for i in range(time_to_run):
            angles = [p.getJointState(robot_id, link_id)[0] for link_id in link_ids]
            if i % 10 == 0:
                moving_directions = network.predict(angles)
                # print("Neural Network Output:", moving_directions)
                for j in range(len(moving_directions)):
                    if moving_directions[j] < 0.4:
                        directions[j] = -0.05
                    elif moving_directions[j] > 0.6:
                        directions[j] = 0.05
                    else:
                        directions[j] = 0

            for j, link_id in enumerate(link_ids):
                p.setJointMotorControl2(robot_id, link_id, p.POSITION_CONTROL,
                                        targetPosition=angles[j] + directions[j],
                                        force=constants.MOTOR_MAX_FORCE,
                                        maxVelocity=constants.MOTOR_MAX_VELOCITY)

            p.stepSimulation()
            if wait is True:
                time.sleep(0.01)

    robot_position, robot_orientation = p.getBasePositionAndOrientation(robot_id)
    distance = -robot_position[0]
    p.resetBasePositionAndOrientation(robot_id, startPos, startOrientation)
    return distance
