#!/usr/bin/env python3
import json

data = []
for i in range(0, 100):
    data.append({"id": i+1, "xPos": i, "yPos": 0,
                 "lightIdx": i, "stripIdx": 0, "next": [i+2]})
for i in range(100, 139):
    data.append({"id": i+1, "xPos": 101, "yPos": 0,
                 "lightIdx": i, "stripIdx": 0, "next": [i+2]})
for i in range(139, 250):
    data.append({"id": i+1, "xPos": i-38, "yPos": 0,
                 "lightIdx": i, "stripIdx": 0, "next": [i+2]})

for i in range(250, 350):
    print(str(i-((i-249)*2 + 61)), ", ", str(25 + i-250))
    data.append({"id": i+1, "xPos": i-((i-249)*2 + 61), "yPos": 25 + i-250,
                 "lightIdx": i, "stripIdx": 0, "next": [i+2]})

for i in range(350, 400+19):
    data.append({"id": i+1, "xPos": i-((i-249)*2 + 61), "yPos": i-((i-249)*2 + 61) + 36,
                 "lightIdx": i, "stripIdx": 0, "next": [i+2]})

data[-1]["next"] = []

out_file = open("wip-config.tmp", "w")
out_file.write(json.dumps(data))
out_file.close()


"""
350     124
351     123

"""
