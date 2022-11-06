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
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

print(os.path.dirname(os.path.realpath(__file__)))


COLOR_RED = Color(0, 255, 0)
COLOR_BLUE = Color(0, 0, 255)
COLOR_GREEN_DIM = Color(150, 0, 0)
COLOR_GREEN = Color(255, 0, 0)
COLOR_DARK_GREEN = Color(180, 0, 0)
COLOR_WHITE = Color(255, 255, 255)
COLOR_OFF_WHITE = Color(248, 240, 200)
COLOR_WHITE_2 = Color(100, 100, 100)
COLOR_OFF = Color(0, 0, 0)
COLOR_PURPLE = Color(40, 140, 225)
COLOR_ORANGE = Color(100, 255, 0)


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

system = LEDSystem(led_count=50)
# system.createConfig()
system.readConfig(os.path.dirname(
    os.path.realpath(__file__)) + "/wip-config.tmp")

system.colorWipeInst(COLOR_PURPLE, True)


system.start()

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


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
