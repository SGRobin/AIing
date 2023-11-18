import time

import pybullet as p
import pybullet_data

import constants
import hard_code_walk
import user_control

physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
p.setGravity(0, 0, -9.81)
planeId = p.loadURDF("plane.urdf")

# Replace 'robot_id.urdf' with your own URDF file path or name
urdf_file_path = "models/crab_model.urdf.xml"

# Load the robot model
startPos = [0, 0, 0.2]
startOrientation = p.getQuaternionFromEuler([0, 0, 0])
robot_id = p.loadURDF(urdf_file_path, startPos, startOrientation)

# for stuff
user_access = False
hard_walk = True

if user_access is True:
    joint_id = user_control.setup_user_control()

check = 0
exit_check = False
while True:
    for link_id in range(31):
        p.changeDynamics(robot_id,
                         link_id,
                         lateralFriction=constants.LINEAR_FRICTION,
                         angularDamping=constants.ANGULAR_FRICTION,
                         frictionAnchor=1)

    if user_access is True:
        user_control.step_user_control(robot_id, joint_id)

    if hard_walk is True:
        check += 1
        hard_code_walk.step(robot_id, check)

    p.stepSimulation()
    time.sleep(1. / 240.)
    if exit_check:
        break

cubePos, cubeOrn = p.getBasePositionAndOrientation(robot_id)
print(cubePos, cubeOrn)
p.disconnect()
