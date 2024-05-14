import time

import numpy as np
import pybullet as p
import pybullet_data
import pybullet_utils.bullet_client as bc

# import Simulation.hard_code_walk as hard
import constants
import global_variables
from constants import PRINT_SIMULATION as PRINT


class Simulation:
    def __init__(self, gui=False):
        self.i = 0
        self.physics_client = bc.BulletClient(connection_mode=p.GUI if gui else p.DIRECT)
        # self.id = simulation_id

        self.link_ids = [2, 3, 4, 7, 8, 9, 12, 13, 14, 17, 18, 19, 22, 23, 24, 27, 28, 29]
        self.URDF_file_path = r"C:\Users\USER\PycharmProjects\AIing\Simulation\models\crab_model.urdf.xml"
        self.startPos = [0, 0, 0.18]
        self.startOrientation = self.physics_client.getQuaternionFromEuler([0, 0, 0])

        self.robot_id = self.physics_client.loadURDF(self.URDF_file_path, self.startPos, self.startOrientation)
        for link_id in self.link_ids:
            self.physics_client.changeDynamics(self.robot_id,
                                               link_id,
                                               # linearDamping=10,
                                               lateralFriction=constants.LINEAR_FRICTION,
                                               # angularDamping=constants.ANGULAR_FRICTION,
                                               # spinningFriction=100,
                                               # contactStiffness=10000,
                                               # jointDamping=0.5,
                                               # contactDamping=10000,
                                               frictionAnchor=1)

        if gui:
            focus_position, _ = self.physics_client.getBasePositionAndOrientation(self.robot_id)
            self.physics_client.resetDebugVisualizerCamera(cameraDistance=1, cameraYaw=135, cameraPitch=-40,
                                                           cameraTargetPosition=focus_position)

        self.physics_client.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.physics_client.setGravity(0, 0, -9.81)

        self.physics_client.setRealTimeSimulation(0)
        # self.physics_client.setTimeStep(1 / 60)

        self.plane_id = self.physics_client.loadURDF("plane.urdf")

        self.collision_dict = {"4": 0, "9": 0, "14": 0, "19": 0, "24": 0, "29": 0}

    def unload_simulation(self, nothing=None):
        self.physics_client.disconnect()

    def reset_joints(self):
        for joint in self.link_ids:
            self.physics_client.resetJointState(self.robot_id, joint, 0)
            self.physics_client.resetBasePositionAndOrientation(self.robot_id, self.startPos, self.startOrientation)

    def punish_positions(self):
        punishment = 0

        robot_position, robot_orientation = self.physics_client.getBasePositionAndOrientation(self.robot_id)
        orientations = self.physics_client.getEulerFromQuaternion(robot_orientation)

        # punishment for being inclined:
        for orientation in orientations:
            punishment += abs(orientation) / 300
            if PRINT:
                self.sum_orientation += abs(orientation) / 300

        # remove reward if too low:
        if robot_position[2] <= 0.8:
            punishment += 0.001
            if PRINT:
                self.sum_low += 0.001
                print("low low low low..")

        # punishment for going sideways:
        punishment += abs(robot_position[1]) / 350
        if PRINT:
            self.sum_position += abs(robot_position[1]) / 350

        # punishment for overbending:
        angles = np.array([self.physics_client.getJointState(self.robot_id, link_id)[0] for link_id in self.link_ids])
        angles = np.degrees(angles) + 90
        # print(angles)
        for i in range(0, 18, 3):
            # print(angles[i + 1], angles[i + 2])
            if angles[i + 1] + angles[i + 2] < 135:
                punishment += 0.001
                if PRINT:
                    print("I am BENDING!!")
                    self.sum_bending += 0.001



        return punishment

    def punish_collisions(self):
        punishment = 0

        collision_points = self.physics_client.getContactPoints(self.robot_id, self.plane_id)
        collision_links = [point[3] for point in collision_points]

        for key in self.collision_dict:
            self.collision_dict[key] += 1

            if (self.collision_dict[key] + 1) % 300 == 0:
                punishment += 0.025
                if PRINT:
                    self.sum_not_all_legs += 0.025
                    print("not using all legs")

        for link in collision_links:
            if self.collision_dict.get(str(link)) is None:
                return 100
            if 2 < self.collision_dict[str(link)] < 20:
                punishment += 0.004
                if PRINT:
                    self.sum_small_steps += 0.004
                    print("small steps... (again)")
            self.collision_dict[str(link)] = 0

        return punishment

    def run_simulation(self, network=None, wait=False, time_to_run=3000):
        self.reset_joints()
        reward = 0
        self.collision_dict = {"4": 0, "9": 0, "14": 0, "19": 0, "24": 0, "29": 0}
        new_angles = [self.physics_client.getJointState(self.robot_id, link_id)[0] for link_id in
                      self.link_ids]
        if PRINT:
            self.sum_not_all_legs = 0
            self.sum_small_steps = 0
            self.sum_orientation = 0
            self.sum_position = 0
            self.sum_low = 0
            self.sum_bending = 0

        for i in range(time_to_run):

            punishment = self.punish_collisions()
            reward -= punishment

            if i % 15 == 0:
                angles = np.array(
                    [self.physics_client.getJointState(self.robot_id, link_id)[0] for link_id in self.link_ids])
                # Scale each element in the angles to the new range of inputs
                inputs = angles * 20 / 3
                # print(inputs)

                outputs = network.predict(inputs)
                # print(outputs)
                new_angles = (np.array(outputs) * 1.2) - 0.6  # [(out * 1.2) - 0.6 for out in outputs]
                # true_angles = [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90]
                # new_angles = np.radians(np.array(true_angles) - 90)

            if i % 45 == 0:
                punishment = self.punish_positions()

                # exit check:
                if punishment == -1:
                    return reward - 100

                reward -= punishment
                # print(reward)

            for j, link_id in enumerate(self.link_ids):
                self.physics_client.setJointMotorControl2(self.robot_id, link_id,
                                                          self.physics_client.POSITION_CONTROL,
                                                          targetPosition=new_angles[j],
                                                          force=constants.MOTOR_MAX_FORCE,
                                                          maxVelocity=constants.MOTOR_MAX_VELOCITY)

            # start_time = time.time()
            self.physics_client.stepSimulation()
            # end_time = time.time()
            # simulation_execution_time += end_time - start_time
            if wait is True:
                time.sleep(0.004)

        robot_position, robot_orientation = self.physics_client.getBasePositionAndOrientation(self.robot_id)
        distance = -robot_position[0]
        reward += distance

        # stop him from staying in place:
        if distance < 0.1:
            reward -= 0.5

        if PRINT:
            print("punishments:")
            print("\tsum not all legs:", self.sum_not_all_legs)
            print("\tsum small steps:", self.sum_small_steps)
            print("\tsum low:", self.sum_low)
            print("\tsum position:", self.sum_position)
            print("\tsum orientation:", self.sum_orientation)
            print("\tsum bending:", self.sum_bending)
        return reward

    #########
    # arduino control with simulation:
    def run_arduino_simulation(self, arduino, network=None, time_to_run=3000):
        self.reset_joints()
        new_angles = [self.physics_client.getJointState(self.robot_id, link_id)[0] for link_id in
                      self.link_ids]

        for i in range(time_to_run):
            angles = np.array(
                [self.physics_client.getJointState(self.robot_id, link_id)[0] for link_id in self.link_ids])

            # pause simulation check:
            if global_variables.PAUSE_ROBOT:
                break

            if i % 10 == 0:
                # arduino control:
                print(python_to_robot_angles(angles))
                arduino.write(bytearray(python_to_robot_angles(angles)))
            # input()
            time.sleep(0.01)
            if i % 15 == 0:
                angles = np.array(
                    [self.physics_client.getJointState(self.robot_id, link_id)[0] for link_id in self.link_ids])

                # Scale each element in the angles to the new range of inputs
                inputs = angles * 20 / 3
                # print(inputs)

                outputs = network.predict(inputs)
                # print(outputs)
                new_angles = [(out * 1.2) - 0.6 for out in outputs]

            for j, link_id in enumerate(self.link_ids):
                self.physics_client.setJointMotorControl2(self.robot_id, link_id,
                                                          self.physics_client.POSITION_CONTROL,
                                                          targetPosition=new_angles[j],
                                                          force=constants.MOTOR_MAX_FORCE,
                                                          maxVelocity=constants.MOTOR_MAX_VELOCITY)

            self.physics_client.stepSimulation()
            # time.sleep(0.01)

        # Return to standing:
        base_angles = [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90]
        arduino.write(bytearray(base_angles))


def python_to_robot_angles(angles):
    # print(outputs)
    angles = np.degrees(angles) + 90
    leg_1 = [angles[15], 180 - angles[16], angles[17]]
    leg_2 = [angles[12], 180 - angles[13], angles[14]]
    leg_3 = [angles[9], 180 - angles[10], angles[11]]
    leg_4 = [angles[0], 180 - angles[1], angles[2]]
    leg_5 = [angles[3], 180 - angles[4], angles[5]]
    leg_6 = [angles[6], 180 - angles[7], angles[8]]
    # leg_1 = [angles[15], angles[16], angles[17]]
    # leg_2 = [angles[12], angles[13], angles[14]]
    # leg_3 = [angles[9], angles[10], angles[11]]
    # leg_4 = [angles[0], angles[1], angles[2]]
    # leg_5 = [angles[3], angles[4], angles[5]]
    # leg_6 = [angles[6], angles[7], angles[8]]
    robot_angles = [leg_1[0], leg_2[0], leg_3[0], leg_4[0], leg_5[0], leg_6[0],
                    leg_1[1], leg_2[1], leg_3[1], leg_4[1], leg_5[1], leg_6[1],
                    leg_1[2], leg_2[2], leg_3[2], leg_4[2], leg_5[2], leg_6[2]]
    # print(f"sending angles {[int(a) for a in robot_angles]}")

    return [int(a) for a in robot_angles]
