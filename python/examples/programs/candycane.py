from programs.program import Program
from rpi_ws281x import Color


class CandyCaneProgram(Program):
    def __init__(self,
                 stripe_length=30,
                 gap_length=30,
                 offset=0,
                 is_reversed=False,
                 speed=1,
                 stripe_rgb=[255, 0, 0],
                 gap_rgb=[255, 255, 255],
                 program_range=None,
                 ):
        super().__init__("candycane", program_range)

        self.stripe_length = stripe_length
        self.gap_length = gap_length
        self.offset = offset
        self.is_reversed = is_reversed
        self.speed = speed
        self.stripe_rgb = stripe_rgb
        self.gap_rgb = gap_rgb

    def update(self, it):
        if self.is_reversed:
            x = -1
        else:
            x = 1

        # Paint the entire gap in one go
        if (self.gap_rgb):
            self.paint(
                Color(self.gap_rgb[0], self.gap_rgb[1], self.gap_rgb[2]))

        cycle = self.stripe_length + self.gap_length

        p = (self.offset + x * it) % cycle - cycle
        while p <= self.system.led_count:
            # p = int(((x * it * self.speed) - (x*i) +
            #          self.offset)) % self.system.led_count
            self.paint(
                Color(
                    int(self.stripe_rgb[0]),
                    int(self.stripe_rgb[1]),
                    int(self.stripe_rgb[2])
                ),
                range(p, p + self.stripe_length)
            )
            p += cycle
