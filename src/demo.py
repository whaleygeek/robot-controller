# demo.py  15/01/2021  D.J.Whale
# Demonstration of robot controller

import sys
if sys.hexversion < 0x00030000:
    exit("Please use python3")

import rcontrol as rc

robot = rc.TextRobot()

while True:
    changed, gear, speed, direction = rc.sense()
    if changed:
        if   gear == rc.FORWARD:    robot.forward(speed)
        elif gear == rc.BACKWARD:   robot.backward(speed)
        elif gear == rc.STOP:       robot.stop()
        robot.steer(direction)

# END
