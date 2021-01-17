# robot.py  15/01/2021  D.J.Whale
# Simple simulation of a robot - replace with your own robot routines.

import turtle
# import thread

class VisualRobot():
    STOP     = "s"
    FORWARD  = "f"
    BACKWARD = "b"
    BOUNCE   = 10

    def __init__(self):
        turtle.forward(0)  # cause turtle canvas to display
        w, h = turtle.screensize()
        self._XMIN = -(w/2)
        self._XMAX = (w/2)
        self._YMIN = -(h/2)
        self._YMAX = h/2

        self._gear  = self.STOP
        self._rate  = 0
        self._steer = 0

    def forward(self, rate:int=10):
        self._gear = self.FORWARD
        self._rate = rate

    def backward(self, rate:int=10):
        self._gear = self.BACKWARD
        self._rate = rate

    def stop(self):
        self._gear = self.STOP
        self._rate = 0
        self._steer = 0

    def steer(self, amount:int=0):
        self._steer = amount

    def move(self):
        if self._gear == self.STOP: return  # no action unless moving

        # Update rotation on each move, based on steering
        # steer is -100..+100 (an integer percentage), 0 is no steer
        if self._steer != 0:
            r = self._steer / 5
            if r < 0:
                turtle.left(-r)
            else:
                turtle.right(r)

        # move forward or backward based on the gear
        speed = self._rate
        if self._gear == self.FORWARD:
            turtle.forward(speed)
        elif self._gear == self.BACKWARD:
            turtle.backward(speed)

        # if it hit the wall, bounce it back
        self.bounce(turtle.xcor(), turtle.ycor())
        #print(self._XMAX, self._YMAX, turtle.xcor(), turtle.ycor())

    def bounce(self, x, y):
        b = False
        if x < self._XMIN:
            x = self._XMIN + self.BOUNCE
            b = True
        elif x > self._XMAX:
            x = self._XMAX - self.BOUNCE
            b = True
        if y < self._YMIN:
            y = self._YMIN + self.BOUNCE
            b = True
        elif y > self._YMAX:
            y = self._YMAX - self.BOUNCE
            b = True

        if b:
            turtle.setpos(x, y)


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


# END
