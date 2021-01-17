# microbit.py  15/01/2021  D.J.Whale
# Simulator for a micro:bit - will be replaced with BITIO

class Radio():
    # RCNNABGRR+SS  (12 chars)
    # 0123456789AB
    TESTDATA = (
        "RC0000F99+00",
        None,
        None,
        "RC0000F00+99",
        "RC0000F99-99",
        "RC0000S00+00",
        "RC0000B99+00",
        "RC0000B99-99",
        "RC0000B99+99"
    )
    def __init__(self):
        self._index = 0

    def receive(self):
        v = self.TESTDATA[self._index]
        self._index += 1
        if self._index >= len(self.TESTDATA):
            self._index = 0
        return v

radio = Radio()

# END
