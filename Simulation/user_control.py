import numpy as np
import pybullet as p


def setup_user_control():
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

    joint_id_dict = {
        1: base_joint,
        2: leg_center_joint_r1,
        3: coxa_joint_r1,
        4: femur_joint_r1,
        5: tibia_joint_r1,
        6: tibia_foot_joint_r1,
        7: leg_center_joint_r2,
        8: coxa_joint_r2,
        9: femur_joint_r2,
        10: tibia_joint_r2,
        11: tibia_foot_joint_r2,
        12: leg_center_joint_r3,
        13: coxa_joint_r3,
        14: femur_joint_r3,
        15: tibia_joint_r3,
        16: tibia_foot_joint_r3,
        17: leg_center_joint_l1,
        18: coxa_joint_l1,
        19: femur_joint_l1,
        20: tibia_joint_l1,
        21: tibia_foot_joint_l1,
        22: leg_center_joint_l2,
        23: coxa_joint_l2,
        24: femur_joint_l2,
        25: tibia_joint_l2,
        26: tibia_foot_joint_l2,
        27: leg_center_joint_l3,
        28: coxa_joint_l3,
        29: femur_joint_l3,
        30: tibia_joint_l3,
        31: tibia_foot_joint_l3,
    }

    return joint_id_dict


def step_user_control(robot_id, joint_id_dict):
    user_angle_base_joint = p.readUserDebugParameter(joint_id_dict.get(1))
    user_angle_leg_center_joint_r1 = p.readUserDebugParameter(joint_id_dict.get(2))
    user_angle_coxa_joint_r1 = p.readUserDebugParameter(joint_id_dict.get(3))
    user_angle_femur_joint_r1 = p.readUserDebugParameter(joint_id_dict.get(4))
    user_angle_tibia_joint_r1 = p.readUserDebugParameter(joint_id_dict.get(5))
    user_angle_tibia_foot_joint_r1 = p.readUserDebugParameter(joint_id_dict.get(6))
    user_angle_leg_center_joint_r2 = p.readUserDebugParameter(joint_id_dict.get(7))
    user_angle_coxa_joint_r2 = p.readUserDebugParameter(joint_id_dict.get(8))
    user_angle_femur_joint_r2 = p.readUserDebugParameter(joint_id_dict.get(9))
    user_angle_tibia_joint_r2 = p.readUserDebugParameter(joint_id_dict.get(10))
    user_angle_tibia_foot_joint_r2 = p.readUserDebugParameter(joint_id_dict.get(11))
    user_angle_leg_center_joint_r3 = p.readUserDebugParameter(joint_id_dict.get(12))
    user_angle_coxa_joint_r3 = p.readUserDebugParameter(joint_id_dict.get(13))
    user_angle_femur_joint_r3 = p.readUserDebugParameter(joint_id_dict.get(14))
    user_angle_tibia_joint_r3 = p.readUserDebugParameter(joint_id_dict.get(15))
    user_angle_tibia_foot_joint_r3 = p.readUserDebugParameter(joint_id_dict.get(16))
    user_angle_leg_center_joint_l1 = p.readUserDebugParameter(joint_id_dict.get(17))
    user_angle_coxa_joint_l1 = p.readUserDebugParameter(joint_id_dict.get(18))
    user_angle_femur_joint_l1 = p.readUserDebugParameter(joint_id_dict.get(19))
    user_angle_tibia_joint_l1 = p.readUserDebugParameter(joint_id_dict.get(20))
    user_angle_tibia_foot_joint_l1 = p.readUserDebugParameter(joint_id_dict.get(21))
    user_angle_leg_center_joint_l2 = p.readUserDebugParameter(joint_id_dict.get(22))
    user_angle_coxa_joint_l2 = p.readUserDebugParameter(joint_id_dict.get(23))
    user_angle_femur_joint_l2 = p.readUserDebugParameter(joint_id_dict.get(24))
    user_angle_tibia_joint_l2 = p.readUserDebugParameter(joint_id_dict.get(25))
    user_angle_tibia_foot_joint_l2 = p.readUserDebugParameter(joint_id_dict.get(26))
    user_angle_leg_center_joint_l3 = p.readUserDebugParameter(joint_id_dict.get(27))
    user_angle_coxa_joint_l3 = p.readUserDebugParameter(joint_id_dict.get(28))
    user_angle_femur_joint_l3 = p.readUserDebugParameter(joint_id_dict.get(29))
    user_angle_tibia_joint_l3 = p.readUserDebugParameter(joint_id_dict.get(30))
    user_angle_tibia_foot_joint_l3 = p.readUserDebugParameter(joint_id_dict.get(31))

    p.setJointMotorControl2(robot_id, 0, p.POSITION_CONTROL, targetPosition=user_angle_base_joint)
    p.setJointMotorControl2(robot_id, 1, p.POSITION_CONTROL, targetPosition=user_angle_leg_center_joint_r1)
    p.setJointMotorControl2(robot_id, 2, p.POSITION_CONTROL, targetPosition=user_angle_coxa_joint_r1)
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
