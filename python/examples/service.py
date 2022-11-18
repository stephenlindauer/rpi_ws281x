#!/usr/bin/env python3

# How to Start/Stop service:
# sudo systemctl start lights
# sudo systemctl stop lights

import asyncio
from rpi_ws281x import Color
from led import LED
from led_system import LEDSystem
from pattern import SimplePattern
from datetime import datetime
from programs.strobe import StrobeProgram
from programs.heartbeat import HeartbeatProgram
from programs.tail import TailProgram
from programs.candycane import CandyCaneProgram
import threading
from wsserver import WebSocketServer
from httpserver import HTTPServerWrapper
import json


def onChange(bulb, color, previous):
    asyncio.run(websocket_server.send(json.dumps({
        "bulb": bulb,
        "color": color
    })))
    # print("Bulb %d changed to %d from %d" % (bulb, color, previous))


system = LEDSystem(led_count=200)
system.onChangeListener = onChange
print("Starting")

system.configure({
    "components": [
        {
            "label": "main_strip",
            "light_begin": "infer",
            "length": "infer",
            "components": [
                {
                    "label": "strip1",
                    "light_begin": 0,
                    "length": 50
                },
                {
                    "label": "strip2",
                    "light_begin": 50,
                    "length": 50
                }
            ]
        },
        {
            "label": "wreath",
            "light_begin": 100,
            "length": 100,
        }
    ]
})
system.start()

main_strip = system.getComponentByName("main_strip")
print("main_strip=", main_strip)
wreath = system.getComponentByName("wreath")
print("wreath=", wreath)


# system.addProgram(StrobeProgram(), 0)
# system.addProgram(HeartbeatProgram(), 10)
system.addProgram(CandyCaneProgram(stripe_length=10, gap_length=30), 11)
# system.addProgram(CandyCaneProgram(stripe_length=10,
#                   gap_length=20, stripe_rgb=[0, 0, 0], gap_rgb=[250, 0, 0], is_reversed=True), 12)

# wreath
system.addProgram(CandyCaneProgram(stripe_length=21,
                  gap_length=4, stripe_rgb=[0, 200, 0], gap_rgb=[255, 255, 50], program_range=range(100, 200)), 12)
system.addProgram(CandyCaneProgram(stripe_length=2, offset=10,
                  gap_length=23, stripe_rgb=[255, 255, 50], gap_rgb=None, program_range=range(100, 200)), 13)

# system.addProgram(TailProgram(
#     length=10, rgb=[0, 255, 0], program_range=range(0, 200)), 15)

# system.addProgram(TailProgram(
#     length=3, rgb=[0, 0, 0], program_range=range(100, 200), is_reversed=True, speed=1.5), 15)

# system.addProgram(TailProgram(length=12, offset=15,
#                   is_reversed=True, speed=1, fade=False, rgb=[0, 0, 255]), 16)

# # Real Pattern below
# it = 0
# print("Starting updates")
# while True:
#     time.sleep(1)
#     it += 1
#     # print("Start loop")
#     if (it % 2 == 0):
#         system.colorWipe(COLOR_RED, True)
#     else:
#         system.colorWipe(COLOR_WHITE, True)

#     time.sleep(1 / 20.0)

#     # system.theaterChase(Color(127, 127, 127))  # White theater chase
#     # system.theaterChase(Color(127,   0,   0))  # Red theater chase
#     # system.theaterChase(Color(0,   0, 127))  # Blue theater chase
#     # system.rainbow()
#     # system.rainbowCycle()
#     # system.theaterChaseRainbow()


def start_webserver():
    HTTPServerWrapper().start()


def start_websocket():
    global websocket_server
    websocket_server = WebSocketServer()
    websocket_server.start()


if __name__ == "__main__":
    http_server = threading.Thread(target=start_webserver, args=())
    ws_server = threading.Thread(target=start_websocket, args=())

    # starting thread 1
    http_server.start()
    # starting thread 2
    ws_server.start()

    # wait until thread 1 is completely executed
    http_server.join()
    # wait until thread 2 is completely executed
    ws_server.join()

    # both threads completely executed
    print("Done!")
