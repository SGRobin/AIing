import numpy as np
import pybullet as p
import time
import pybullet_data

physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
p.setGravity(0, 0, -9.81)
planeId = p.loadURDF("plane.urdf")

# Replace 'robot_id.urdf' with your own URDF file path or name
urdf_file_path = "models/bike.urdf"


startPos = [0, 0, 1]
startOrientation = p.getQuaternionFromEuler([0, 0, 0])
robot_id = p.loadURDF(urdf_file_path, startPos, startOrientation)

while True:
    p.stepSimulation()
    time.sleep(1. / 240.)