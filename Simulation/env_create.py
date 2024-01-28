import time

import numpy as np
# import cupy as np
import pybullet as p
import pybullet_data

import Simulation.hard_code_walk as hard
import constants

link_ids = [2, 3, 4, 7, 8, 9, 12, 13, 14, 17, 18, 19, 22, 23, 24, 27, 28, 29]
URDF_file_path = "C:\\Users\\USER\\PycharmProjects\\AIing\\Simulation\\models\\crab_model.urdf.xml"
startPos = [0, 0, 0.18]
startOrientation = p.getQuaternionFromEuler([0, 0, 0])
robot_id = None


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def load_simulation(gui=False):
    p.connect(p.GUI if gui else p.DIRECT)  # or p.DIRECT for non-graphical version

    global robot_id
    robot_id = p.loadURDF(URDF_file_path, startPos, startOrientation)
    for link_id in link_ids:
        p.changeDynamics(robot_id,
                         link_id,
                         lateralFriction=constants.LINEAR_FRICTION,
                         angularDamping=constants.ANGULAR_FRICTION,
                         frictionAnchor=1)

    if gui:
        focus_position, _ = p.getBasePositionAndOrientation(robot_id)
        p.resetDebugVisualizerCamera(cameraDistance=1, cameraYaw=135, cameraPitch=-40,
                                     cameraTargetPosition=focus_position)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
    p.setGravity(0, 0, -9.81)

    p.setRealTimeSimulation(0)
    p.setTimeStep(1 / 60)
    # p.setPhysicsEngineParameter(numSolverIterations=3)
    # p.setPhysicsEngineParameter(numSubSteps=1)
    # p.setPhysicsEngineParameter(contactERP=0.9, frictionERP=0.2)
    p.loadURDF("plane.urdf")


def unload_simulation():
    p.disconnect()


def reset_joints():
    for joint in link_ids:
        p.resetJointState(robot_id, joint, 0)


simulations_ran = 0.0
total_time = 0.0


def run_simulation(network=None, wait=False, time_to_run=3000, network_controlled=True, hard_walk=False):
    global total_time, simulations_ran
    reset_joints()
    directions = [0] * 18

    if network_controlled is True:
        for i in range(time_to_run):
            angles = [p.getJointState(robot_id, link_id)[0] for link_id in link_ids]

            if i % 10 == 0:
                moving_directions = network.predict(angles)
                directions = [-0.02 if d < 0.4 else 0.02 if d > 0.6 else 0 for d in moving_directions]

                if i % 50 == 0:
                    robot_position, robot_orientation = p.getBasePositionAndOrientation(robot_id)
                    if abs(robot_orientation[3]) < 0.95:
                        distance = -robot_position[0]
                        p.resetBasePositionAndOrientation(robot_id, startPos, startOrientation)
                        return distance - 1

            for j, link_id in enumerate(link_ids):
                p.setJointMotorControl2(robot_id, link_id, p.POSITION_CONTROL,
                                        targetPosition=angles[j] + directions[j],
                                        force=constants.MOTOR_MAX_FORCE,
                                        maxVelocity=constants.MOTOR_MAX_VELOCITY)

            # start_time = time.time()
            p.stepSimulation()
            # end_time = time.time()
            # simulation_execution_time += end_time - start_time
            if wait is True:
                time.sleep(0.004)

    else:
        for i in range(time_to_run):
            hard.step(robot_id, i)
            p.stepSimulation()
            if wait is True:
                time.sleep(0.001)
    # print(f"simulation_execution_time: {simulation_execution_time} seconds\n")

    robot_position, robot_orientation = p.getBasePositionAndOrientation(robot_id)
    distance = -robot_position[0]
    p.resetBasePositionAndOrientation(robot_id, startPos, startOrientation)
    return distance
