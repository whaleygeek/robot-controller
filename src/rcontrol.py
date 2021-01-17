# rcontrol.py  15/01/2021  D.J.Whale
# Remote controller for a robot, using a micro:bit

import sys
if sys.hexversion < 0x03000000:
    exit("Please use python3")

import time
##import microbit_mock as microbit  # simulated microbit use
import microbit  # bitio use

microbit.radio.on()

FORWARD  = "F"
BACKWARD = "B"
STOP     = "S"
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
    UNIQUE = "RC"  # unique code for this controller

    def receive(self):
        return microbit.radio.receive()

    def decode(self, payload) -> tuple or None:
        # gear(SFB), rate(0..99), steer(-99..99)
        # RCNNABGRR+SS  (12 chars)
        # 0123456789AB

        if len(payload) < 12: return None
        if payload[0:2] != self.UNIQUE: return None

        ##seqno    = payload[2:4]
        ##button_a = True if payload[4] == "1" else False
        ##button_b = True if payload[5] == "1" else False
        gear     = payload[6]
        try:
            rate     = int(payload[7:9])
            steer    = int(payload[9:12])
        except:
            return None # invalid payload

        return gear, rate, steer

    def sense(self) -> tuple or None:  # gear(SFB, rate(0..99), steer(-99..99)
        payload = self.receive()
        if payload is None: return None
        return self.decode(payload)


tg = TimingGate(TICKSEC)
controller = Controller()
gear, rate, steer = STOP, 0, 0


#----- API ---------------------------------------------------------------------

def sense() -> tuple:  # (changed, gear, speed, direction)
    """Sense the controller values"""
    global gear, rate, steer

    changed = False
    if tg():
        print("TICK")
        values = controller.sense()
        if values is not None:
            g, r, s = values
            if g != gear:
                gear = g
                changed = True
            if r != rate:
                rate = r
                changed = True
            if s != steer:
                steer = s
                changed = True

    return changed, gear, rate, steer


# END
