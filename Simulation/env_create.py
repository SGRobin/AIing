import numpy as np
import pybullet as p
import time
import pybullet_data

physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
p.setGravity(0, 0, 0)
planeId = p.loadURDF("plane.urdf")

# Replace 'robot_id.urdf' with your own URDF file path or name
urdf_file_path = "../Simulation/models/crab_model.urdf"


startPos = [0, 0, 1]
startOrientation = p.getQuaternionFromEuler([0, 0, 0])
robot_id = p.loadURDF(urdf_file_path, startPos, startOrientation)


# For user accessibility
base_joint = p.addUserDebugParameter('base_joint', -np.pi / 2, np.pi / 2, 0)
leg_center_joint_r1 = p.addUserDebugParameter('leg_center_joint_r1', -np.pi / 2, np.pi / 2, 0)
coxa_joint_r1 = p.addUserDebugParameter('coxa_joint_r1', -np.pi / 2, np.pi / 2, 0)
femur_joint_r1 = p.addUserDebugParameter('femur_joint_r1', -np.pi / 2, np.pi / 2, 0)
tibia_joint_r1 = p.addUserDebugParameter('tibia_joint_r1', -np.pi / 2, np.pi / 2, 0)
tibia_foot_joint_r1 = p.addUserDebugParameter('tibia_foot_joint_r1', -np.pi / 2, np.pi / 2, 0)
leg_center_joint_r2 = p.addUserDebugParameter('leg_center_joint_r2', -np.pi / 2, np.pi / 2, 0)
coxa_joint_r2 = p.addUserDebugParameter('coxa_joint_r2', -np.pi / 2, np.pi / 2, 0)
femur_joint_r2 = p.addUserDebugParameter('femur_joint_r2', -np.pi / 2, np.pi / 2, 0)
tibia_joint_r2 = p.addUserDebugParameter('tibia_joint_r2', -np.pi / 2, np.pi / 2, 0)
tibia_foot_joint_r2 = p.addUserDebugParameter('tibia_foot_joint_r2', -np.pi / 2, np.pi / 2, 0)
leg_center_joint_r3 = p.addUserDebugParameter('leg_center_joint_r3', -np.pi / 2, np.pi / 2, 0)
coxa_joint_r3 = p.addUserDebugParameter('coxa_joint_r3', -np.pi / 2, np.pi / 2, 0)
femur_joint_r3 = p.addUserDebugParameter('femur_joint_r3', -np.pi / 2, np.pi / 2, 0)
tibia_joint_r3 = p.addUserDebugParameter('tibia_joint_r3', -np.pi / 2, np.pi / 2, 0)
tibia_foot_joint_r3 = p.addUserDebugParameter('tibia_foot_joint_r3', -np.pi / 2, np.pi / 2, 0)
leg_center_joint_l1 = p.addUserDebugParameter('leg_center_joint_l1', -np.pi / 2, np.pi / 2, 0)
coxa_joint_l1 = p.addUserDebugParameter('coxa_joint_l1', -np.pi / 2, np.pi / 2, 0)
femur_joint_l1 = p.addUserDebugParameter('femur_joint_l1', -np.pi / 2, np.pi / 2, 0)
tibia_joint_l1 = p.addUserDebugParameter('tibia_joint_l1', -np.pi / 2, np.pi / 2, 0)
tibia_foot_joint_l1 = p.addUserDebugParameter('tibia_foot_joint_l1', -np.pi / 2, np.pi / 2, 0)
leg_center_joint_l2 = p.addUserDebugParameter('leg_center_joint_l2', -np.pi / 2, np.pi / 2, 0)
coxa_joint_l2 = p.addUserDebugParameter('coxa_joint_l2', -np.pi / 2, np.pi / 2, 0)
femur_joint_l2 = p.addUserDebugParameter('femur_joint_l2', -np.pi / 2, np.pi / 2, 0)
tibia_joint_l2 = p.addUserDebugParameter('tibia_joint_l2', -np.pi / 2, np.pi / 2, 0)
tibia_foot_joint_l2 = p.addUserDebugParameter('tibia_foot_joint_l2', -np.pi / 2, np.pi / 2, 0)
leg_center_joint_l3 = p.addUserDebugParameter('leg_center_joint_l3', -np.pi / 2, np.pi / 2, 0)
coxa_joint_l3 = p.addUserDebugParameter('coxa_joint_l3', -np.pi / 2, np.pi / 2, 0)
femur_joint_l3 = p.addUserDebugParameter('femur_joint_l3', -np.pi / 2, np.pi / 2, 0)
tibia_joint_l3 = p.addUserDebugParameter('tibia_joint_l3', -np.pi / 2, np.pi / 2, 0)
tibia_foot_joint_l3 = p.addUserDebugParameter('tibia_foot_joint_l3', -np.pi / 2, np.pi / 2, 0)

check = 0
exit_check = False
while True:
    user_angle_base_joint = p.readUserDebugParameter(base_joint)
    user_angle_leg_center_joint_r1 = p.readUserDebugParameter(leg_center_joint_r1)
    user_angle_coxa_joint_r1 = p.readUserDebugParameter(coxa_joint_r1)
    user_angle_femur_joint_r1 = p.readUserDebugParameter(femur_joint_r1)
    user_angle_tibia_joint_r1 = p.readUserDebugParameter(tibia_joint_r1)
    user_angle_tibia_foot_joint_r1 = p.readUserDebugParameter(tibia_foot_joint_r1)
    user_angle_leg_center_joint_r2 = p.readUserDebugParameter(leg_center_joint_r2)
    user_angle_coxa_joint_r2 = p.readUserDebugParameter(coxa_joint_r2)
    user_angle_femur_joint_r2 = p.readUserDebugParameter(femur_joint_r2)
    user_angle_tibia_joint_r2 = p.readUserDebugParameter(tibia_joint_r2)
    user_angle_tibia_foot_joint_r2 = p.readUserDebugParameter(tibia_foot_joint_r2)
    user_angle_leg_center_joint_r3 = p.readUserDebugParameter(leg_center_joint_r3)
    user_angle_coxa_joint_r3 = p.readUserDebugParameter(coxa_joint_r3)
    user_angle_femur_joint_r3 = p.readUserDebugParameter(femur_joint_r3)
    user_angle_tibia_joint_r3 = p.readUserDebugParameter(tibia_joint_r3)
    user_angle_tibia_foot_joint_r3 = p.readUserDebugParameter(tibia_foot_joint_r3)
    user_angle_leg_center_joint_l1 = p.readUserDebugParameter(leg_center_joint_l1)
    user_angle_coxa_joint_l1 = p.readUserDebugParameter(coxa_joint_l1)
    user_angle_femur_joint_l1 = p.readUserDebugParameter(femur_joint_l1)
    user_angle_tibia_joint_l1 = p.readUserDebugParameter(tibia_joint_l1)
    user_angle_tibia_foot_joint_l1 = p.readUserDebugParameter(tibia_foot_joint_l1)
    user_angle_leg_center_joint_l2 = p.readUserDebugParameter(leg_center_joint_l2)
    user_angle_coxa_joint_l2 = p.readUserDebugParameter(coxa_joint_l2)
    user_angle_femur_joint_l2 = p.readUserDebugParameter(femur_joint_l2)
    user_angle_tibia_joint_l2 = p.readUserDebugParameter(tibia_joint_l2)
    user_angle_tibia_foot_joint_l2 = p.readUserDebugParameter(tibia_foot_joint_l2)
    user_angle_leg_center_joint_l3 = p.readUserDebugParameter(leg_center_joint_l3)
    user_angle_coxa_joint_l3 = p.readUserDebugParameter(coxa_joint_l3)
    user_angle_femur_joint_l3 = p.readUserDebugParameter(femur_joint_l3)
    user_angle_tibia_joint_l3 = p.readUserDebugParameter(tibia_joint_l3)
    user_angle_tibia_foot_joint_l3 = p.readUserDebugParameter(tibia_foot_joint_l3)

    p.setJointMotorControl2(robot_id, 0, p.POSITION_CONTROL, targetPosition=user_angle_base_joint)
    p.setJointMotorControl2(robot_id, 1, p.POSITION_CONTROL, targetPosition=user_angle_leg_center_joint_r1)
    # p.setJointMotorControl2(robot_id, 2, p.POSITION_CONTROL, targetPosition=user_angle_coxa_joint_r1)
    p.setJointMotorControl2(robot_id, 3, p.POSITION_CONTROL, targetPosition=user_angle_femur_joint_r1)
    p.setJointMotorControl2(robot_id, 4, p.POSITION_CONTROL, targetPosition=user_angle_tibia_joint_r1)
    p.setJointMotorControl2(robot_id, 5, p.POSITION_CONTROL, targetPosition=user_angle_tibia_foot_joint_r1)
    p.setJointMotorControl2(robot_id, 6, p.POSITION_CONTROL, targetPosition=user_angle_leg_center_joint_r2)
    p.setJointMotorControl2(robot_id, 7, p.POSITION_CONTROL, targetPosition=user_angle_coxa_joint_r2)
    p.setJointMotorControl2(robot_id, 8, p.POSITION_CONTROL, targetPosition=user_angle_femur_joint_r2)
    p.setJointMotorControl2(robot_id, 9, p.POSITION_CONTROL, targetPosition=user_angle_tibia_joint_r2)
    p.setJointMotorControl2(robot_id, 10, p.POSITION_CONTROL, targetPosition=user_angle_tibia_foot_joint_r2)
    p.setJointMotorControl2(robot_id, 11, p.POSITION_CONTROL, targetPosition=user_angle_leg_center_joint_r3)
    p.setJointMotorControl2(robot_id, 12, p.POSITION_CONTROL, targetPosition=user_angle_coxa_joint_r3)
    p.setJointMotorControl2(robot_id, 13, p.POSITION_CONTROL, targetPosition=user_angle_femur_joint_r3)
    p.setJointMotorControl2(robot_id, 14, p.POSITION_CONTROL, targetPosition=user_angle_tibia_joint_r3)
    p.setJointMotorControl2(robot_id, 15, p.POSITION_CONTROL, targetPosition=user_angle_tibia_foot_joint_r3)
    p.setJointMotorControl2(robot_id, 16, p.POSITION_CONTROL, targetPosition=user_angle_leg_center_joint_l1)
    p.setJointMotorControl2(robot_id, 17, p.POSITION_CONTROL, targetPosition=user_angle_coxa_joint_l1)
    p.setJointMotorControl2(robot_id, 18, p.POSITION_CONTROL, targetPosition=user_angle_femur_joint_l1)
    p.setJointMotorControl2(robot_id, 19, p.POSITION_CONTROL, targetPosition=user_angle_tibia_joint_l1)
    p.setJointMotorControl2(robot_id, 20, p.POSITION_CONTROL, targetPosition=user_angle_tibia_foot_joint_l1)
    p.setJointMotorControl2(robot_id, 21, p.POSITION_CONTROL, targetPosition=user_angle_leg_center_joint_l2)
    p.setJointMotorControl2(robot_id, 22, p.POSITION_CONTROL, targetPosition=user_angle_coxa_joint_l2)
    p.setJointMotorControl2(robot_id, 23, p.POSITION_CONTROL, targetPosition=user_angle_femur_joint_l2)
    p.setJointMotorControl2(robot_id, 24, p.POSITION_CONTROL, targetPosition=user_angle_tibia_joint_l2)
    p.setJointMotorControl2(robot_id, 25, p.POSITION_CONTROL, targetPosition=user_angle_tibia_foot_joint_l2)
    p.setJointMotorControl2(robot_id, 26, p.POSITION_CONTROL, targetPosition=user_angle_leg_center_joint_l3)
    p.setJointMotorControl2(robot_id, 27, p.POSITION_CONTROL, targetPosition=user_angle_coxa_joint_l3)
    p.setJointMotorControl2(robot_id, 28, p.POSITION_CONTROL, targetPosition=user_angle_femur_joint_l3)
    p.setJointMotorControl2(robot_id, 29, p.POSITION_CONTROL, targetPosition=user_angle_tibia_joint_l3)
    p.setJointMotorControl2(robot_id, 30, p.POSITION_CONTROL, targetPosition=user_angle_tibia_foot_joint_l3)

    check += 1
    if check % 500 == 0:
        p.setJointMotorControl2(robot_id, 2, p.POSITION_CONTROL, targetPosition=1.5)
    if check % 1000 == 0:
        p.setJointMotorControl2(robot_id, 2, p.POSITION_CONTROL, targetPosition=-1.5)

    p.stepSimulation()
    time.sleep(1. / 240.)
    if exit_check:
        break

cubePos, cubeOrn = p.getBasePositionAndOrientation(robot_id)
print(cubePos, cubeOrn)
p.disconnect()