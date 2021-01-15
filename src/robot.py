# robot.py  15/01/2021  D.J.Whale
# Simple simulation of a robot - replace with your own robot routines.

import turtle

class VisualRobot():
    def __init__(self):
        turtle.forward(0)  # cause turtle canvas to display
        w, h = turtle.screensize()
        self._XMIN = -(w/2)
        self._XMAX = (w/2)
        self._YMIN = -(h/2)
        self._YMAX = h/2

    def forward(self, speed:int=10):
        turtle.forward(speed)

    def backward(self, speed:int=10):
        turtle.backward(speed)

    def stop(self):
        pass

    def steer(self, direction:int=0):
        # direction is -100..+100 (an integer percentage), 0 is no steer
        if direction != 0:
            direction /= 5
            if direction < 0:
                turtle.left(direction)
            else:
                turtle.right(direction)

            self.check_edges(turtle.xcor(), turtle.ycor())
            #print(self._XMAX, self._YMAX, turtle.xcor(), turtle.ycor())

    def check_edges(self, x, y):
        bounce = False
        BOUNCE = 10
        if x < self._XMIN:
            x = self._XMIN + BOUNCE
            bounce = True
        elif x > self._XMAX:
            x = self._XMAX - BOUNCE
            bounce = True
        if y < self._YMIN:
            y = self._YMIN + BOUNCE
            bounce = True
        elif y > self._YMAX:
            y = self._YMAX - BOUNCE
            bounce = True

        if bounce:
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
