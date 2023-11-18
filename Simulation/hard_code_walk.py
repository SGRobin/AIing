import pybullet as p
import constants


def step(robot_id, check):
    p.setJointMotorControl2(robot_id, 0, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)
    p.setJointMotorControl2(robot_id, 1, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)
    p.setJointMotorControl2(robot_id, 4, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)
    p.setJointMotorControl2(robot_id, 5, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)
    p.setJointMotorControl2(robot_id, 6, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)
    p.setJointMotorControl2(robot_id, 9, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)
    p.setJointMotorControl2(robot_id, 10, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)
    p.setJointMotorControl2(robot_id, 11, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)
    p.setJointMotorControl2(robot_id, 14, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)
    p.setJointMotorControl2(robot_id, 15, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)
    p.setJointMotorControl2(robot_id, 16, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)
    p.setJointMotorControl2(robot_id, 19, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)
    p.setJointMotorControl2(robot_id, 20, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)
    p.setJointMotorControl2(robot_id, 21, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)
    p.setJointMotorControl2(robot_id, 24, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)
    p.setJointMotorControl2(robot_id, 25, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)
    p.setJointMotorControl2(robot_id, 26, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)
    p.setJointMotorControl2(robot_id, 29, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)
    p.setJointMotorControl2(robot_id, 30, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                            maxVelocity=constants.MOTOR_MAX_VELOCITY)

    if check % 50 == 0:
        # Down:
        p.setJointMotorControl2(robot_id, 3, p.POSITION_CONTROL, targetPosition=-0.5, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)
        p.setJointMotorControl2(robot_id, 13, p.POSITION_CONTROL, targetPosition=-0.5, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)
        p.setJointMotorControl2(robot_id, 23, p.POSITION_CONTROL, targetPosition=-0.5, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)
        p.setJointMotorControl2(robot_id, 8, p.POSITION_CONTROL, targetPosition=-0.5, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)
        p.setJointMotorControl2(robot_id, 18, p.POSITION_CONTROL, targetPosition=-0.5, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)
        p.setJointMotorControl2(robot_id, 28, p.POSITION_CONTROL, targetPosition=-0.5, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)

    if 50 > check % 200 > 0:
        # UP:
        p.setJointMotorControl2(robot_id, 3, p.POSITION_CONTROL, targetPosition=0.5, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)
        p.setJointMotorControl2(robot_id, 13, p.POSITION_CONTROL, targetPosition=0.5, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)
        p.setJointMotorControl2(robot_id, 23, p.POSITION_CONTROL, targetPosition=0.5, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)

        # MOVE:
        p.setJointMotorControl2(robot_id, 7, p.POSITION_CONTROL, targetPosition=-0.5, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)
        p.setJointMotorControl2(robot_id, 17, p.POSITION_CONTROL, targetPosition=0.5, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)
        p.setJointMotorControl2(robot_id, 27, p.POSITION_CONTROL, targetPosition=0.5, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)

        p.setJointMotorControl2(robot_id, 2, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)
        p.setJointMotorControl2(robot_id, 12, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)
        p.setJointMotorControl2(robot_id, 22, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)

    if 150 > check % 200 > 100:
        # UP:
        p.setJointMotorControl2(robot_id, 8, p.POSITION_CONTROL, targetPosition=0.5, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)
        p.setJointMotorControl2(robot_id, 18, p.POSITION_CONTROL, targetPosition=0.5, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)
        p.setJointMotorControl2(robot_id, 28, p.POSITION_CONTROL, targetPosition=0.5, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)

        # MOVE:
        p.setJointMotorControl2(robot_id, 2, p.POSITION_CONTROL, targetPosition=-0.5, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)
        p.setJointMotorControl2(robot_id, 12, p.POSITION_CONTROL, targetPosition=-0.5, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)
        p.setJointMotorControl2(robot_id, 22, p.POSITION_CONTROL, targetPosition=0.5, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)

        p.setJointMotorControl2(robot_id, 7, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)
        p.setJointMotorControl2(robot_id, 17, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)
        p.setJointMotorControl2(robot_id, 27, p.POSITION_CONTROL, targetPosition=0, force=constants.MOTOR_MAX_FORCE,
                                maxVelocity=constants.MOTOR_MAX_VELOCITY)
