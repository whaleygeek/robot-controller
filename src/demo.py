# demo.py  15/01/2021  D.J.Whale
# Demonstration of robot controller

import sys
if sys.hexversion < 0x03000000:
    exit("Please use python3")

import time

import rcontrol as remote
import robot

robbie = robot.VisualRobot()

def forward(rate=100):
    # change this to move your robot forward
    robbie.forward(rate)

def backward(rate=100):
    # change this to move your robot backward
    robbie.backward(rate)

def stop():
    # change this to stop your robot
    robbie.stop()

def steer(pos=0):
    # change this to steer your robot
    robbie.steer(pos)

while True:
    changed, g, r, s = remote.sense()
    if changed:
        if   g == remote.FORWARD:    forward(r)
        elif g == remote.BACKWARD:   backward(r)
        elif g == remote.STOP:       stop()
        steer(s)
    robbie.move() ## TODO do with a thread in robot.py
    time.sleep(0.1)
    
# END
