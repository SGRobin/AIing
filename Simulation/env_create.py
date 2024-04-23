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

    def punishments(self):
        punishment = 0

        robot_position, robot_orientation = self.physics_client.getBasePositionAndOrientation(self.robot_id)
        orientations = self.physics_client.getEulerFromQuaternion(robot_orientation)

        # punishment for being inclined:
        for orientation in orientations:
            punishment += abs(orientation) / 40

        # remove reward if too low:
        if robot_position[2] <= 0.06:
            punishment += 0.01

        collision_points = self.physics_client.getContactPoints(self.robot_id, self.plane_id)
        #
        # # punishment for going sideways - legs:
        # for point in collision_points:
        #     if point[5][1] > 0.3:
        #         punishment += 0.01

        # punishment for going sideways:
        # todo: only when smart already only like that
        punishment += abs(robot_position[1]) / 30

        # punishment for not using all legs
        collision_links = [point[3] for point in collision_points]
        for key in self.collision_dict:
            self.collision_dict[key] += 1
            if self.collision_dict[key] > 15:
                punishment += 0.01
        for link in collision_links:
            self.collision_dict[str(link)] = 0

        # stop simulation if he is tilted
        # if abs(robot_orientation[3]) < 0.98:
        #     self.physics_client.resetBasePositionAndOrientation(self.robot_id, self.startPos,
        #                                                         self.startOrientation)
        #     return - 1
        return punishment / 4.0

    def run_simulation(self, network=None, wait=False, time_to_run=3000, network_controlled=True):
        self.reset_joints()
        reward = 0
        self.collision_dict = {"4": 0, "9": 0, "14": 0, "19": 0, "24": 0, "29": 0}
        if network_controlled is True:
            new_angles = [self.physics_client.getJointState(self.robot_id, link_id)[0] for link_id in
                          self.link_ids]
            for i in range(time_to_run):

                if i % 15 == 0:
                    angles = np.array(
                        [self.physics_client.getJointState(self.robot_id, link_id)[0] for link_id in self.link_ids])
                    # Scale each element in the angles to the new range of inputs
                    inputs = angles * 20 / 3
                    # print(inputs)

                    outputs = network.predict(inputs)
                    print(outputs)
                    new_angles = [(out * 1.2) - 0.6 for out in outputs]

                if i % 45 == 0:
                    punishment = self.punishments()

                    # exit check:
                    if punishment == -1:
                        return reward - 100

                    reward -= punishment

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

        else:
            for i in range(time_to_run):
                hard.step(self.robot_id, i)
                self.physics_client.stepSimulation()
                if i % 45 == 0:
                    punishment = self.punishments()

                    # exit check:
                    if punishment == -1:
                        return reward - 100

                    reward -= punishment
                if wait is True:
                    time.sleep(0.004)

        robot_position, robot_orientation = self.physics_client.getBasePositionAndOrientation(self.robot_id)
        distance = -robot_position[0]
        reward += distance

        # stop him from staying in place:
        if distance < 0.1:
            reward -= 0.5

        return reward

    #########
    # arduino control with simulation:
    def run_arduino_simulation(self, arduino, network=None, time_to_run=3000):
        self.reset_joints()
        new_angles = [self.physics_client.getJointState(self.robot_id, link_id)[0] for link_id in
                      self.link_ids]

        for i in range(time_to_run):

            if i % 15 == 0:
                angles = np.array(
                    [self.physics_client.getJointState(self.robot_id, link_id)[0] for link_id in self.link_ids])
                # Scale each element in the angles to the new range of inputs
                inputs = angles * 20 / 3
                # print(inputs)

                outputs = network.predict(inputs)
                print(outputs)
                new_angles = [(out * 1.2) - 0.6 for out in outputs]

                # arduino control:
                angles = python_to_robot_angles(outputs)
                arduino.write(bytearray([*([angles[0]] * 6), *([angles[1]] * 6), *([angles[2]] * 6)]))

                for _ in range(18):
                    arduino.read()

            for j, link_id in enumerate(self.link_ids):
                self.physics_client.setJointMotorControl2(self.robot_id, link_id,
                                                          self.physics_client.POSITION_CONTROL,
                                                          targetPosition=new_angles[j],
                                                          force=constants.MOTOR_MAX_FORCE,
                                                          maxVelocity=constants.MOTOR_MAX_VELOCITY)

            self.physics_client.stepSimulation()
            time.sleep(0.01)


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
