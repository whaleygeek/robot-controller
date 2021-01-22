# demo.py  15/01/2021  D.J.Whale
# Demonstration of robot controller

import sys
if sys.hexversion < 0x03000000:
    exit("Please use python3")

import time

import rcontrol as remote
import robot

robby = robot.VisualRobot()  # From: Forbidden Planet, 1956.

def forward(speed=100):
    # change this to move your robot forward
    robby.forward(speed)

def backward(speed=100):
    # change this to move your robot backward
    robby.backward(speed)

def stop():
    # change this to stop your robot
    robby.stop()

def steer(direction=0):
    # change this to steer your robot
    robby.steer(direction)

while True:
    changed, gear, speed, direction = remote.sense()
    if changed:
        if   gear == remote.FORWARD:    forward(speed)
        elif gear == remote.BACKWARD:   backward(speed)
        elif gear == remote.STOP:       stop()
        steer(direction)
    robby.move()
    time.sleep(0.1)

# END
