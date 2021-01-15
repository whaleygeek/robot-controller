# rcontrol.py  15/01/2021  D.J.Whale
# Remote controller for a robot, using a micro:bit

import sys
if sys.hexversion < 0x03000000:
    exit("Please use python3")

import time
import random

FORWARD  = "f"
BACKWARD = "b"
STOP     = "s"
MAXACC   = 1000
DEADZONE = 100
MAXSPEED = 100
MAXDIRN  = 100


class Microbit:
    """scaffolding due to no micro:bit added yet (BITIO)"""
    class Accelerometer:
        _VALUES = ((0, 0, 0), (200, 200, 0), (0, 0, 0), (300, -300, 0))
        _index = 0
        def get_values(self) -> tuple:  # x, y, z
            values = self._VALUES[self._index]
            self._index += 1
            if self._index >= len(self._VALUES):
                self._index = 0
            return values

    accelerometer = Accelerometer()

microbit = Microbit()

class TimingGate():
    """A way to generate timing ticks cooperatively"""
    def __init__(self, rate: float = 0.1):
        self._rate = rate
        self._next = time.time() + rate

    def __call__(self) -> bool:
        """Check if the next timing gate has occurred"""
        now = time.time()

        if now < self._next:
            return False
        self._next = now + self._rate
        return True


# class VisualRobot():
#     def __init__(self):
#         pass
#
#     def forward(self, speed: int = 100):
#         pass
#
#     def backward(self, speed: int = 100):
#         pass
#
#     def steer(self, direction: int = 0):
#         pass


class TextRobot():
    """A simulation of a robot that just prints messages"""
    @staticmethod
    def _say(msg:str) -> None:
        print(msg)

    def stop(self):
        self._say("STOP")

    def forward(self, speed:int=100):
        self._say("FORWARD:%d" % speed)

    def backward(self, speed:int=100):
        self._say("BACKWARD:%d" % speed)

    def steer(self, direction:int=0):
        self._say("STEER:%d" % direction)


class Controller():
    """A model of a hand controller, handles transforms from tilt to commands"""

    @staticmethod
    def _limit(v:int, limit:int) -> int:
        if v > limit: return limit
        if v < -limit: return -limit
        return v

    @staticmethod
    def _calculate(x:int, y:int) -> tuple:
        x = Controller._limit(x, MAXACC)
        y = Controller._limit(y, MAXACC)

        if abs(x) < DEADZONE \
        or abs(y) < DEADZONE:
            return STOP, 0, 0

        s = abs(x) * MAXSPEED / MAXACC
        d = y      * MAXDIRN  / MAXACC

        if x > 0:
            return FORWARD, s, d
        else:
            return BACKWARD, s, d

    def sense(self) -> tuple:
        x, y, z = microbit.accelerometer.get_values()
        return self._calculate(x, y)

tg = TimingGate(1)
controller = Controller()
gear, speed, direction = STOP, 0, 0


#----- API ---------------------------------------------------------------------

def sense() -> tuple:  # (changed, gear, speed, direction)
    """Sense the controller values"""
    global gear, speed, direction

    changed = False
    if tg():
        print("TICK")
        g, s, d = controller.sense()
        if g != gear:
            gear = g
            changed = True
        if s != speed:
            speed = s
            changed = True
        if d != direction:
            direction = d
            changed = True

    return changed, gear, speed, direction


# END
