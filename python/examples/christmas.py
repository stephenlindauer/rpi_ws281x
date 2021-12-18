#!/usr/bin/env python3

import time
from rpi_ws281x import Color
import argparse
import math
from led import LED
from led_system import LEDSystem
import sys
from pattern import SimplePattern
import os

print(os.path.dirname(os.path.realpath(__file__)))


COLOR_RED = Color(0, 255, 0)
COLOR_BLUE = Color(0, 0, 255)
COLOR_GREEN = Color(255, 0, 0)
COLOR_DARK_GREEN = Color(180, 0, 0)
COLOR_WHITE = Color(255, 255, 255)
COLOR_OFF = Color(0, 0, 0)


def colorWipe(strip, color, wait_ms=10):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def colorWipeInst(strip, color, wait_ms=10):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()


# Process arguments
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--skip-startup', action='store_true',
                    help='Clear startup animation')
args = parser.parse_args()


# Startup Animation (flash solid green 3X)
# colorWipeInst(strip, COLOR_OFF)
# if not args.skip_startup:
#     colorWipe(strip, COLOR_GREEN, 1)
#     time.sleep(0.2)
#     colorWipeInst(strip, COLOR_OFF)
#     time.sleep(0.2)
#     colorWipeInst(strip, COLOR_GREEN)
#     time.sleep(0.2)
#     colorWipeInst(strip, COLOR_OFF)
#     time.sleep(0.2)
#     colorWipeInst(strip, COLOR_GREEN)
#     time.sleep(0.2)
#     colorWipeInst(strip, COLOR_OFF)
#     time.sleep(0.2)
#     colorWipeInst(strip, COLOR_GREEN)
#     time.sleep(0.2)
#     colorWipeInst(strip, COLOR_OFF)

system = LEDSystem()
# system.createConfig()
system.readConfig(os.path.dirname(
    os.path.realpath(__file__)) + "/wip-config.tmp")

system.colorWipeInst(COLOR_OFF, True)

# # Test Pattern
# while True:
#     p = SimplePattern(
#         [
#             # COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF,
#             COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED,
#             COLOR_BLUE, COLOR_BLUE, COLOR_BLUE, COLOR_BLUE, COLOR_BLUE, COLOR_BLUE, COLOR_BLUE, COLOR_BLUE,
#             COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE,
#         ])
#     system.paintPatternOld(p, 600, 500)
# # END OF TEST PATTERN

# Real Pattern below
while True:
    print("Start loop")
    system.configureBrightness()

    # Red White Green pattern
    # p = SimplePattern(
    #     [COLOR_WHITE, COLOR_GREEN, COLOR_RED])
    # system.paintPatternOld(p, 10, 100)
    p = SimplePattern(
        [COLOR_WHITE, COLOR_WHITE, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN])
    system.paintPatternCounterClockwise(p, 10, 100)
    p.setColors(
        [COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN])
    system.paintPatternCounterClockwise(p, 10, 100)
    p.setColors(
        [COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN])
    system.paintPatternCounterClockwise(p, 10, 100)
    p.setColors(
        [COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN])
    system.paintPatternCounterClockwise(p, 10, 100)
    p.setColors(
        [COLOR_RED, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN])
    system.paintPatternCounterClockwise(p, 10, 100)
    p.setColors(
        [COLOR_RED, COLOR_RED, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_DARK_GREEN, COLOR_DARK_GREEN, COLOR_DARK_GREEN])
    system.paintPatternCounterClockwise(p, 10, 100)
    p.setColors(
        [COLOR_RED, COLOR_RED, COLOR_RED, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_DARK_GREEN, COLOR_DARK_GREEN])
    system.paintPatternCounterClockwise(p, 10, 100)
    p.setColors(
        [COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_DARK_GREEN])
    system.paintPatternCounterClockwise(p, 10, 100)
    p.setColors(
        [COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE])
    system.paintPatternCounterClockwise(p, 10, 100)

    p = SimplePattern(
        [COLOR_WHITE, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_WHITE, COLOR_RED, COLOR_RED, COLOR_RED])
    system.paintPatternOld(p, 100, 100)
    # p = SimplePattern(
    #     [COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED])
    # system.paintPatternOld(p, 10, 100)

    p = SimplePattern([COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_WHITE,
                       COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE])
    system.paintPatternCounterClockwise(p, 60, 100)
    # system.paintPatternRight(p, 60, 200)

    p = SimplePattern(
        [COLOR_BLUE, COLOR_BLUE, COLOR_BLUE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE])
    system.paintPatternOld(p, 60, 100)

    p = SimplePattern(
        [COLOR_RED, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF])
    system.paintPatternOld(p, 10, 100)
    p = SimplePattern(
        [COLOR_WHITE, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF])
    system.paintPatternOld(p, 10, 100)
    p = SimplePattern(
        [COLOR_RED, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF])
    system.paintPatternCounterClockwise(p, 10, 100)
    p = SimplePattern(
        [COLOR_WHITE, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF, COLOR_OFF])
    system.paintPatternCounterClockwise(p, 10, 100)
    system.colorWipeInst(COLOR_OFF)
    delay = 10
    system.colorWipe(COLOR_WHITE, delay)
    system.colorWipe(COLOR_RED, delay)
    system.colorWipe(COLOR_GREEN, delay)


# tip = 93
# tip_led = LED(strip, tip, 50, 100)
# last_left = tip_led
# last_right = tip_led
# system.addLED(tip_led)

# for i in range(1, 20):
#     n = LED(strip, tip+i, 50+i, 100-i)
#     p = LED(strip, tip-i, 50-i, 100-i)
#     n.addPrevious(last_right)
#     p.addNext(last_left)
#     last_right = n
#     last_left = p
#     system.addLED(n)
#     system.addLED(p)

# last_left.addPrevious(last_right)

# last_right = tip_led
# for i in range(0, 15):
#     n = LED(strip, 130-i, 85-i, 100-i)
#     n.addPrevious(last_right)
#     last_right = n
#     system.addLED(n)

d = 100
while True:
    # system.theaterChase(Color(127, 127, 127))  # White theater chase
    # system.theaterChase(Color(127,   0,   0))  # Red theater chase
    # system.theaterChase(Color(0,   0, 127))  # Blue theater chase
    # system.rainbow()
    # system.rainbowCycle()
    # system.theaterChaseRainbow()

    system.coverRightByPosition(COLOR_BLUE, d)
    system.coverLeftByPosition(COLOR_OFF, d)
    system.coverLeftByPosition(COLOR_WHITE, d)
    system.coverRightByPosition(COLOR_BLUE, d)
    system.coverLeftByPosition(COLOR_WHITE, d)

    system.coverDownByPosition(COLOR_RED, d)
    system.coverUpByPosition(COLOR_GREEN, d)
    system.coverDownByPosition(COLOR_RED, d)
    system.coverUpByPosition(COLOR_GREEN, d)
    # system.coverNextByNeighbor(system.lights[0], COLOR_RED, d)
    system.coverUpByPosition(COLOR_OFF, d)
    p = SimplePattern([COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_WHITE,
                       COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE])
    system.paintPatternRight(p, 10, 100)
    # p.setColors([COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_WHITE, COLOR_WHITE,
    #             COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE])
    # system.paintPatternRight(p, 0.1, 100)
    # p.setColors([COLOR_RED, COLOR_RED, COLOR_RED, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE,
    #             COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE])
    # system.paintPatternRight(p, 0.1, 100)
    # p.setColors([COLOR_RED, COLOR_RED, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE,
    #             COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE])
    # system.paintPatternRight(p, 0.1, 100)
    # p.setColors([COLOR_RED, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE,
    #             COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE])
    # system.paintPatternRight(p, 0.1, 100)
    # p.setColors([COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE,
    #             COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE])
    # system.paintPatternRight(p, 0.1, 100)
