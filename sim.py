import math
import os
from pathlib import Path
from time import sleep
import json
import matplotlib.pyplot as plt
import numpy as np
    #initialise world boundaries
canvasY = 30000
canvasX = 40000

    #ask input prefs
prefs = int(input("Enter 1 to open a JSON or 2 to enter raw data:"))

if prefs == 1:
        #ask for file input
    filedir = Path(__file__).parent
    file = input('Input file name:')
    if len(file) < 1:
        file = filedir / 'dataDefault.json'
    try:
        fileRead = open(file, 'r')
    except:
        print("File opening failed")
        exit()
    data = json.load(fileRead)
    redforV = float(data['redfor']['speed_mps'])
    redforAltInit = float(data['redfor']['altitude_m'])
    redforXInit = float(data['redfor']['x_position_m'])

    bluforV = float(data['blufor']['speed_mps'])
    bluforAltInit = float(data['blufor']['altitude_m'])
    bluforXInit = float(data['blufor']['x_position_m'])

    missileV = float(data['missile']['speed_mps'])

if prefs == 2:
        # initialise redfor's physics
    redforV = input("input redfor's speed in m/s:")
    try: redforV = float(redforV)
    except:
        print("redfor's speed must be a number.")

    redforAltInit = input("input redfor's altitude in metres:")
    try: redforAltInit = float(redforAltInit)
    except:
        print("redfor's altitude must be a number.")
    if redforAltInit > 30000 or redforAltInit < 0:
        print("redfor's alt must be between 0 and 30000 metres.")

    redforXInit = input("input redfor's X position in metres:")
    try: redforXInit = float(redforXInit)
    except:
        print("redfor's X position must be a number.")
    if redforXInit > 40000 or redforXInit < 0:
        print("redfor's X position musy be between 0 and 40000 metres.")

        #initialise blufor's physics

    bluforV = input("input blufor's speed in m/s:")
    try: bluforV = float(bluforV)
    except:
        print("blufor's speed must be a number.")

    bluforAltInit = input("input blufor's altitude in metres:")
    try: bluforAltInit = float(bluforAltInit)
    except:
        print("blufor's altitude must be a number.")
    if bluforAltInit > 30000 or bluforAltInit < 0:
        print("bluefor's altitude must be between 0 and 30000 metres.")

    bluforXInit = input("input blufor's X position in metres:")
    try: bluforXInit = float(bluforXInit)
    except:
        print("blufor's X position must be a number.")
    if bluforXInit > 40000 or bluforXInit < 0:
        print("blufor's X position must be between 0 and 40000 metres.")

        #initialise missile physics
    missileV = input("input missile's speed in m/s")
    try: missileV = float(missileV)
    except:
        print("missile's speed must be a number")



    #flight
redforAlt = redforAltInit
bluforAlt = bluforAltInit
redforX = redforXInit
bluforX = bluforXInit

missileAlt = bluforAlt
missileX = bluforX


dx = redforX - missileX
dy = redforAlt - missileAlt
missileDistance = math.hypot(dx, dy)

def distanceCalc():
    dx = redforX - bluforX
    dy = redforAlt - bluforAlt
    airDistance = math.hypot(dx, dy)
    return airDistance

def missileCalc():
    dx = redforX - missileX
    dy = redforAlt - missileAlt
    missileDistance = math.hypot(dx, dy)
    return missileDistance

    #inertia
def missileInertia():
    if count > 500:
        missileVNew = missileV * 0.99985
        return missileVNew
    else:
        return missileV        

    #plotting
count = 0
x = np.array([bluforXInit])
y = np.array([bluforAltInit])
redX = np.array([redforXInit])
redY = np.array([redforAltInit])
bluX = np.array([bluforXInit])
bluY = np.array([bluforAltInit])

plt.ion()
fig, ax = plt.subplots()
ax.set_xlim(0, canvasX)
ax.set_ylim(0, canvasY)
missileGraph, = ax.plot(x, y, 'c')
redforGraph, = ax.plot(redX, redY, 'r')
bluforGraph, = ax.plot(bluX, bluY, 'b')
ax.set_xlabel('Downrange (m)')
ax.set_ylabel('Altitude (m)')
plt.legend(['Missile', 'Redfor', 'Blufor'])

    #missile flight
oldMissileDistance = missileDistance
while missileDistance > 50:
    count += 1
    missileV = missileInertia()
    uX = (redforX - missileX) / missileDistance
    uY = (redforAlt - missileAlt) / missileDistance
    redforX = redforX - (redforV * 0.01)
    missileX = missileX + (missileV * uX * 0.01)
    missileAlt = missileAlt + (missileV * uY * 0.01)
    missileDistance = missileCalc()

    bluforX = bluforX + (bluforV * 0.01)



    if oldMissileDistance < missileDistance:
        print("Missile has lost lock")
        end()
    oldMissileDistance = missileDistance
    if count % 10 == 0:
        print(f"{count/100} S"
              f"\n\n{missileX:8.1f} m downrange\n"
              f"{missileAlt:8.1f} m altitude\n"
              f"{missileDistance:8.1f} m from target\n"
              f"{missileV:8.1f} m/s")
    if count % 10 == 0:
        x = np.append(x, missileX)
        y = np.append(y, missileAlt)
        redX = np.append(redX, redforX)
        redY = np.append(redY, redforAlt)
        bluX = np.append(bluX, bluforX)
        bluY = np.append(bluY, bluforAlt)
        
        missileGraph.set_data(x, y)
        redforGraph.set_data(redX, redY)
        bluforGraph.set_data(bluX, bluY)
        fig.canvas.draw()
        fig.canvas.flush_events()
    time = count / 100

    sleep(0.0)
    continue

print("Missile has proxy fused")
print(time, "seconds of flight time")
plt.ioff()
plt.show()
