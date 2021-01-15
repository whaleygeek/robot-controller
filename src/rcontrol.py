# rcontrol.py  15/01/2021  D.J.Whale
# Remote controller for a robot, using a micro:bit

import sys
if sys.hexversion < 0x00030000:
    exit("Please use python3")

import time

class microbit:
    """scaffolding due to no micro:bit added yet (BITIO)"""
    class accelerometer:
        @staticmethod
        def get_values() -> tuple:  # x, y, z
            return 0, 0, 0

FORWARD  = "f"
BACKWARD = "b"
STOP     = "s"

class TimingGate():
    """A way to generate timing ticks cooperatively"""
    def __init__(self, ratems: int = 100):
        self._ratems = ratems
        self._next = time.time() + ratems

    def __call__(self) -> bool:
        """Check if the next timing gate has occurred"""
        now = time.time()
        if now < self._next:
            return False
        self._next = now + self._ratems
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

    def forward(self, speed:int=100):
        self._say("FORWARD:%d" % speed)

    def backward(self, speed:int=100):
        self._say("BACKWARD:%d" % speed)

    def steer(self, direction:int=0):
        self._say("STEER:%d" % direction)


class Controller():
    """A model of a hand controller, handles transforms from tilt to commands"""
    DEADZONE = 100
    MAXACC   = 1000
    MAXSPEED = 100
    MAXDIRN  = 100

    @staticmethod
    def _limit(v:int, limit:int) -> int:
        if v > limit: return limit
        if v < -limit: return -limit
        return v

    @staticmethod
    def _calculate(x:int, y:int) -> tuple:
        x = Controller._limit(x, Controller.MAXACC)
        y = Controller._limit(y, Controller.MAXACC)

        if abs(x) < Controller.DEADZONE \
        or abs(y) < Controller.DEADZONE:
            return STOP, 0, 0

        speed = abs(x) * Controller.MAXSPEED / Controller.MAXACC
        direction = y * Controller.MAXDIRN / Controller.MAXACC

        if x > 0:
            return FORWARD, speed, direction
        else:
            return BACKWARD, speed, direction

    def sense(self) -> tuple:
        x, y, z = microbit.accelerometer.get_values()
        return self._calculate(x, y)

tg = TimingGate()
controller = Controller()
gear, speed, direction = STOP, 0, 0


#----- API ---------------------------------------------------------------------

def sense() -> tuple:  # (changed, gear, speed, direction)
    """Sense the controller values"""
    global gear, speed, direction

    changed = False
    if tg():
        gear, speed, direction = controller.sense()
        changed = True

    return changed, gear, speed, direction


# END
