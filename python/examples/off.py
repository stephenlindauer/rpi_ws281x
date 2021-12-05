#!/usr/bin/env python3

import time
from rpi_ws281x import Color
import argparse
import math
from led import LED
from led_system import LEDSystem
import sys


COLOR_OFF = Color(0, 0, 0)


system = LEDSystem()
# system.createConfig()
system.readConfig()

system.colorWipeInst(COLOR_OFF)
