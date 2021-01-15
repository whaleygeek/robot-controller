# rcontrol.py  15/01/2021  D.J.Whale
# Remote controller for a robot, using a micro:bit

import sys
if sys.hexversion < 0x03000000:
    exit("Please use python3")

import time
import microbit

FORWARD  = "f"
BACKWARD = "b"
STOP     = "s"
MAXACC   = 1000
DEADZONE = 100
MAXSPEED = 100
MAXDIRN  = 100
TICKSEC  = 0.1


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

tg = TimingGate(TICKSEC)
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
