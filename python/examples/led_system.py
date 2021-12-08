import time
from rpi_ws281x import Color, Adafruit_NeoPixel
import argparse
import math
from led import LED
import json

COLOR_RED = Color(0, 255, 0)
COLOR_BLUE = Color(0, 0, 255)
COLOR_GREEN = Color(255, 0, 0)
COLOR_WHITE = Color(200, 200, 200)
COLOR_OFF = Color(0, 0, 0)


class LEDSystem:
    max_x = float('-inf')
    max_y = float('-inf')
    min_x = float('inf')
    min_y = float('inf')
    strip = None

    def __init__(self, led_count=519, skip_intro=False):
        # LED strip configuration:
        # LED_COUNT = 100      # Number of LED pixels.
        # 18      # GPIO pin connected to the pixels (18 uses PWM!).
        LED_PIN = 12
        # LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA = 10      # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 100
        # Set to 0 for darkest and 255 for brightest
        # True to invert the signal (when using NPN transistor level shift)
        LED_INVERT = False
        LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

        self.strip = Adafruit_NeoPixel(led_count, LED_PIN, LED_FREQ_HZ,
                                       LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()

        self.lights = []
        self.nextId = 1

        # if not skip_intro:
        # self.colorWipeInst(COLOR_OFF)
        # self.colorWipe(COLOR_GREEN, 20)
        # self.colorWipeInst(COLOR_OFF)

        # while True:
        #     self.colorWipe(COLOR_RED, 50)
        #     self.colorWipe(COLOR_GREEN, 50)
        #     self.colorWipe(COLOR_WHITE, 50)

    """
    Goes through each LED on the strip and stores data about it to a config
    """

    def storeConfig(self, filename):
        out = []
        for led in self.lights:
            out.append(led.serialize())
        out_file = open(filename, "w")
        out_file.write(json.dumps(out))
        out_file.close()

    def createConfig(self, resume_from_last=None):
        self.colorWipeInst(COLOR_OFF)

        last_pos = None
        last_led = None
        start = 0
        if resume_from_last:
            self.readConfig("wip-config.tmp")
            print(self.led_mapping[resume_from_last])
            last_led = self.led_mapping[resume_from_last]
            last_pos = resume_from_last
            start = resume_from_last+1
            self.nextId = resume_from_last

        for i in range(start, self.strip.numPixels()):
            self.storeConfig("wip-config.tmp")
            self.colorWipeInst(COLOR_OFF)
            self.strip.setPixelColor(i-2, COLOR_WHITE)
            self.strip.setPixelColor(i-1, COLOR_WHITE)
            self.strip.setPixelColor(i, COLOR_RED)
            self.strip.show()
            print(f"Lit up bulb #{i}")
            if last_pos:
                print(f"Last position was: {last_pos}")

            pos = None
            while True:
                pos = input("Position (or mark x,y / clear): ")
                if pos.startswith("mark "):
                    try:
                        (x, y) = pos[5:].split(",")
                        self.lightY(int(y), COLOR_BLUE)
                        self.lightX(int(x), COLOR_GREEN)
                    except Exception:
                        print("...huh?")
                elif pos == "clear":
                    self.colorWipeInst(COLOR_OFF)
                elif pos == "list":
                    for l in self.lights:
                        print(l.serialize())
                else:
                    try:
                        (x, y) = pos.split(",")
                        led = LED(self.strip, self.nextId, i, int(x), int(y))
                        self.nextId += 1
                        if last_led:
                            last_led.addNext(led)
                        last_pos = pos
                        break
                    except Exception as e:
                        print("Exception: " + e)
                        print("Unsure if last LED saved or not")

            self.addLED(led)
            last_led = led

        print("Finished mapping strip.")
        if input("Write to file? ") == "y":
            self.storeConfig("config")

    def readConfig(self, config_name="config"):
        print("Opening config " + config_name)
        in_file = open(config_name, "r")
        data = json.loads(in_file.read())
        leds = {}
        # Create LED objects
        for d in data:
            led = LED(self.strip, d["id"], d["lightIdx"],
                      int(d["xPos"]), int(d["yPos"]))
            leds[led.id] = led
            self.addLED(led)
        # Add neighbors
        for d in data:
            led = leds[d["id"]]
            for id in d["next"]:
                next = leds[id]
                led.addNext(next)
        self.led_mapping = leds

    def colorWipe(self, color, wait_ms=10):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def colorWipeInst(self, color):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def theaterChase(self, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, color)
                self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, 0)

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i+j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def rainbowCycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(
                    i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, self.wheel((i+j) % 255))
                self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, 0)

    def addLED(self, led):
        self.lights.append(led)
        self.max_x = max(self.max_x, led.xPos)
        self.max_y = max(self.max_y, led.yPos)
        self.min_x = min(self.min_x, led.xPos)
        self.min_y = min(self.min_y, led.yPos)

    def lightX(self, xPos, color):
        for l in self.lights:
            if l.xPos == xPos:
                l.setColor(color)
        self.strip.show()

    def lightY(self, yPos, color):
        for l in self.lights:
            if l.yPos == yPos:
                l.setColor(color)
        self.strip.show()

    def coverRightByPosition(self, color, delay=20):
        for x in range(self.min_x, self.max_x+1):
            self.lightX(x, color)
            time.sleep(delay/1000.0)

    def coverLeftByPosition(self, color, delay=20):
        for x in range(self.max_x, self.min_x-1, -1):
            self.lightX(x, color)
            time.sleep(delay/1000.0)

    def coverDownByPosition(self, color, delay=20):
        for y in range(self.max_y, self.min_y-1, -1):
            for l in self.lights:
                if l.yPos == y:
                    l.setColor(color)
            self.strip.show()
            time.sleep(delay/1000.0)

    def coverUpByPosition(self, color, delay=20):
        for y in range(self.min_y, self.max_y+1):
            for l in self.lights:
                if l.yPos == y:
                    l.setColor(color)
            self.strip.show()
            time.sleep(delay/1000.0)

    def coverNextByNeighbor(self, first, color, delay=20):
        nexts = [first]
        i = 0
        while i < 100:  # TODO: How long should this run?
            i = i+1
            upcoming_nexts = []
            for next in nexts:
                next.setColor(color)
                upcoming_nexts.extend(next.next)
            self.strip.show()
            time.sleep(delay/1000.0)
            nexts = upcoming_nexts

    def paintPatternRight(self, pattern, duration_s=60, delay_ms=20):
        t = 0
        while t < duration_s * 1000.0:
            for x in range(self.min_x, self.max_x+1):
                color = pattern.getColor(x)
                for l in self.lights:
                    if l.xPos == x:
                        l.setColor(color)

            self.strip.show()
            pattern.bump()
            time.sleep(delay_ms/1000.0)
            t += delay_ms

    def paintPatternOld(self, pattern, duration_s=60, delay_ms=20):
        t = 0
        while t < duration_s * 1000.0:
            for i in range(self.strip.numPixels()):
                color = pattern.getColor(i)
                self.strip.setPixelColor(i, color)

            self.strip.show()
            pattern.bump()
            time.sleep(delay_ms/1000.0)
            t += delay_ms
