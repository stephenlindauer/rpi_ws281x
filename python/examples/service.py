#!/usr/bin/env python3

# How to Start/Stop service:
# sudo systemctl start lights
# sudo systemctl stop lights

import time
from rpi_ws281x import Color
import argparse
import math
from led import LED
from led_system import LEDSystem
import sys
from pattern import SimplePattern
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from programs.strobe import StrobeProgram
from programs.heartbeat import HeartbeatProgram
from programs.tail import TailProgram
from programs.candycane import CandyCaneProgram


system = LEDSystem(led_count=200)
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
system.addProgram(CandyCaneProgram(stripe_length=10, gap_length=50), 11)
# system.addProgram(CandyCaneProgram(stripe_length=10,
#                   gap_length=20, stripe_rgb=[0, 0, 255], gap_rgb=[0, 0, 0], is_reversed=True), 12)

# wreath
# system.addProgram(CandyCaneProgram(stripe_length=21,
#                   gap_length=4, stripe_rgb=[0, 200, 0], gap_rgb=[255, 255, 50], program_range=range(100, 200)), 12)
# system.addProgram(CandyCaneProgram(stripe_length=2, offset=10,
#                   gap_length=23, stripe_rgb=[255, 255, 50], gap_rgb=None, program_range=range(100, 200)), 13)

# system.addProgram(TailProgram(
#     length=10, rgb=[255, 0, 0], program_range=range(0, 200)), 15)

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


# Start Webserver
hostName = "0.0.0.0"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print("do_get")

        if (self.path == "/"):
            self.handleIndex()
        elif (self.path.startswith("/api/")):
            self.handleAPIRequest()
        else:
            self.handle404()

    def handleIndex(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(
            bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def handleAPIRequest(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        (_, api, endpoint, type) = self.path.split("/")
        if (endpoint == 'animation'):
            self.handleAnimation(type)
        self.wfile.write(
            bytes(json.dumps({"status": "OK"}), "utf-8"))

    def handleAnimation(self, animationType):
        system.setAnimation(animationType)

    def handle404(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            bytes("<html><head><title>404</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>Page not found</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


# if __name__ == "__main__":
#     webServer = HTTPServer((hostName, serverPort), MyServer)
#     print("Server started http://%s:%s" % (hostName, serverPort))

#     try:
#         webServer.serve_forever()
#     except KeyboardInterrupt:
#         pass

#     webServer.server_close()
#     print("Server stopped.")
