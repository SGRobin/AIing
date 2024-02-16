import time

import numpy as np
import pybullet as p
import pybullet_data
import pybullet_utils.bullet_client as bc

import Simulation.hard_code_walk as hard
import constants


class Simulation:
    def __init__(self, gui=False):
        self.physics_client = bc.BulletClient(connection_mode=p.GUI if gui else p.DIRECT)
        # self.id = simulation_id

        self.link_ids = [2, 3, 4, 7, 8, 9, 12, 13, 14, 17, 18, 19, 22, 23, 24, 27, 28, 29]
        self.URDF_file_path = "C:\\Users\\USER\\PycharmProjects\\AIing\\Simulation\\models\\crab_model.urdf.xml"
        self.startPos = [0, 0, 0.18]
        self.startOrientation = self.physics_client.getQuaternionFromEuler([0, 0, 0])

        self.robot_id = self.physics_client.loadURDF(self.URDF_file_path, self.startPos, self.startOrientation)
        for link_id in self.link_ids:
            self.physics_client.changeDynamics(self.robot_id,
                                               link_id,
                                               lateralFriction=constants.LINEAR_FRICTION,
                                               angularDamping=constants.ANGULAR_FRICTION,
                                               frictionAnchor=1)

        if gui:
            focus_position, _ = self.physics_client.getBasePositionAndOrientation(self.robot_id)
            self.physics_client.resetDebugVisualizerCamera(cameraDistance=1, cameraYaw=135, cameraPitch=-40,
                                                           cameraTargetPosition=focus_position)

        self.physics_client.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.physics_client.setGravity(0, 0, -9.81)

        self.physics_client.setRealTimeSimulation(0)
        self.physics_client.setTimeStep(1 / 60)

        self.physics_client.loadURDF("plane.urdf")

    def unload_simulation(self, nothing=None):
        self.physics_client.disconnect()

    def reset_joints(self):
        for joint in self.link_ids:
            self.physics_client.resetJointState(self.robot_id, joint, 0)
            self.physics_client.resetBasePositionAndOrientation(self.robot_id, self.startPos, self.startOrientation)

    def run_simulation(self, network=None, wait=False, time_to_run=1500, network_controlled=True):
        self.reset_joints()
        reward = 0
        distance = 0
        if network_controlled is True:
            corrected_angles = [self.physics_client.getJointState(self.robot_id, link_id)[0] for link_id in
                                self.link_ids]
            for i in range(time_to_run):

                if i % 15 == 0:
                    angles = np.array([self.physics_client.getJointState(self.robot_id, link_id)[0] for link_id in self.link_ids])
                    # print(angles)
                    moving_directions = network.predict(angles)
                    directions = [(d / 2.5) - 0.2 for d in moving_directions]
                    corrected_angles = [angles[i] + directions[i] for i in range(len(angles))]

                if i % 45 == 0:
                    robot_position, robot_orientation = self.physics_client.getBasePositionAndOrientation(self.robot_id)
                    # give the reward

                    reward += -robot_position[0] - distance
                    if robot_position[2] <= 0.07:
                        reward -= 0.01

                    distance = -robot_position[0]
                    if abs(robot_orientation[3]) < 0.98:
                        self.physics_client.resetBasePositionAndOrientation(self.robot_id, self.startPos,
                                                                            self.startOrientation)
                        return distance - 1

                for j, link_id in enumerate(self.link_ids):
                    self.physics_client.setJointMotorControl2(self.robot_id, link_id,
                                                              self.physics_client.POSITION_CONTROL,
                                                              targetPosition=corrected_angles[j],
                                                              force=constants.MOTOR_MAX_FORCE,
                                                              maxVelocity=constants.MOTOR_MAX_VELOCITY)

                # start_time = time.time()
                self.physics_client.stepSimulation()
                # end_time = time.time()
                # simulation_execution_time += end_time - start_time
                if wait is True:
                    time.sleep(0.004)

        else:
            for i in range(time_to_run):
                hard.step(self.robot_id, i)
                self.physics_client.stepSimulation()
                if i % 45 == 0:
                    print(reward)
                    robot_position, robot_orientation = self.physics_client.getBasePositionAndOrientation(self.robot_id)
                    # give the reward

                    reward += -robot_position[0] - distance
                    if robot_position[2] <= 0.07:
                        reward -= 0.01

                    distance = -robot_position[0]
                    if abs(robot_orientation[3]) < 0.98:
                        self.physics_client.resetBasePositionAndOrientation(self.robot_id, self.startPos,
                                                                            self.startOrientation)
                        return distance - 1
                if wait is True:
                    time.sleep(0.004)
        # print(f"simulation_execution_time: {simulation_execution_time} seconds\n")

        # robot_position, robot_orientation = p.getBasePositionAndOrientation(robot_id)
        # distance = -robot_position[0]
        # p.resetBasePositionAndOrientation(robot_id, startPos, startOrientation)
        return reward
