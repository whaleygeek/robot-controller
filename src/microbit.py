# microbit.py  15/01/2021  D.J.Whale
# Simulator for a micro:bit - will be replaced with BITIO

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

# END
