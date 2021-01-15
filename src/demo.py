# demo.py  15/01/2021  D.J.Whale
# Demonstration of robot controller

import sys
if sys.hexversion < 0x03000000:
    exit("Please use python3")

import rcontrol as rc
import robot

robbie = robot.VisualRobot()

while True:
    changed, gear, speed, direction = rc.sense()
    if changed:
        if   gear == rc.FORWARD:    robbie.forward(speed)
        elif gear == rc.BACKWARD:   robbie.backward(speed)
        elif gear == rc.STOP:       robbie.stop()
        robbie.steer(direction)


# END
