from programs.program import Program
from rpi_ws281x import Color


class TailProgram(Program):
    def __init__(self, length=30, offset=0, is_reversed=False, speed=1, rgb=[255, 255, 255], fade=True):
        super().__init__("tail")

        self.length = length
        self.offset = offset
        self.is_reversed = is_reversed
        self.speed = speed
        self.rgb = rgb
        self.fade = fade

    def update(self, it):
        if self.is_reversed:
            x = -1
        else:
            x = 1

        for i in range(0, self.length):
            p = int(((x * it * self.speed) - (x*i) +
                     self.offset)) % self.system.led_count
            pct = (1 - i / self.length) if self.fade else 1
            self.paint(
                Color(
                    int(self.rgb[0] * pct),
                    int(self.rgb[1] * pct),
                    int(self.rgb[2] * pct)
                ),
                range(p, p + 1)
            )
