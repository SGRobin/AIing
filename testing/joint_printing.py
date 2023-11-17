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
urdf_file_path = "../Simulation/models/crab_model.urdf.xml"


startPos = [0, 0, 1]
startOrientation = p.getQuaternionFromEuler([0, 0, 0])
robot_id = p.loadURDF(urdf_file_path, startPos, startOrientation)

num_joints = p.getNumJoints(robot_id)
print(num_joints)

name_list = []
for joint_index in range(num_joints):
    joint_info = p.getJointInfo(robot_id, joint_index)
    name_list.append(joint_info[1])

for name in name_list:
    print(f"{name.decode('utf-8')} = p.addUserDebugParameter('{name.decode('utf-8')}', -np.pi / 2, np.pi / 2, 0)")
    print(f"user_angle_{name.decode('utf-8')} = p.readUserDebugParameter({name.decode('utf-8')})")

id = 0
for name in name_list:
    print(f"p.setJointMotorControl2(robot_id, {id}, p.POSITION_CONTROL, targetPosition=user_angle_{name.decode('utf-8')})")
    id += 1

# set the center of mass frame (loadURDF sets base link frame)
# startPos/Ornp.resetBasePositionAndOrientation(robot_id, startPos, startOrientation)

cubePos, cubeOrn = p.getBasePositionAndOrientation(robot_id)
print(cubePos, cubeOrn)
p.disconnect()
