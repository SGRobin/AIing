import os
import subprocess
import numpy as np
import pybullet as p
import time
import pybullet_data

physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
p.setGravity(0, 0, 0)
planeId = p.loadURDF("plane.urdf")

# Replace 'robot_id.urdf' with your own URDF file path or name
urdf_file_path = "models/crab_model.urdf"
robot_id = p.loadURDF(urdf_file_path)
num_joints = p.getNumJoints(robot_id)
startPos = [0, 0, 1]
startOrientation = p.getQuaternionFromEuler([0, 0, 0])


print(num_joints)

for joint_index in range(num_joints):
    joint_info = p.getJointInfo(robot_id, joint_index)
    # joint_info contains information about the joint
    print(joint_info)


# link_states = p.getLinkStates(robot_id, range(num_joints))
# for link_state in link_states:
#     link_position, link_orientation, _, _ = link_state
#     # Use link_position and link_orientation


# set the center of mass frame (loadURDF sets base link frame)
# startPos/Ornp.resetBasePositionAndOrientation(robot_id, startPos, startOrientation)

for i in range(10000):
    p.stepSimulation()
    time.sleep(1. / 240.)

cubePos, cubeOrn = p.getBasePositionAndOrientation(robot_id)
print(cubePos, cubeOrn)
p.disconnect()
