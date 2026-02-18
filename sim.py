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
    redforYInit = float(data['redfor']['altitude_m'])
    redforXInit = float(data['redfor']['x_position_m'])

    bluforV = float(data['blufor']['speed_mps'])
    bluforYInit = float(data['blufor']['altitude_m'])
    bluforXInit = float(data['blufor']['x_position_m'])

    missileV = float(data['missile']['speed_mps'])

if prefs == 2:
        # initialise redfor's physics
    redforV = input("input redfor's speed in m/s:")
    try: redforV = float(redforV)
    except:
        print("redfor's speed must be a number.")

    redforYInit = input("input redfor's altitude in metres")
    try: redforYInit = float(redforYInit)
    except:
        print("redfor's altitude must be a number.")
    if redforYInit > 30000 or redforYInit < 0:
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

    bluforYInit = input("input blufor's altitude in metres:")
    try: bluforYInit = float(bluforYInit)
    except:
        print("blufor's altitude must be a number.")
    if bluforYInit > 30000 or bluforYInit < 0:
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
redforY = redforYInit
bluforAlt = bluforYInit
redforX = redforXInit
bluforX = bluforXInit

missileY = bluforAlt
missileX = bluforX


dx = redforX - missileX
dy = redforY - missileY
missileDistance = math.hypot(dx, dy)

oldUX = None
oldUY = None
missileLaunchV = None
lostLock = 0
lockBreakCount = 0
launchTime = 0

def distanceCalc():
    dx = redforX - bluforX
    dy = redforY - bluforAlt
    airDistance = math.hypot(dx, dy)
    return airDistance

def missileCalc():
    dx = redforX - missileX
    dy = redforY - missileY
    missileDistance = math.hypot(dx, dy)
    return missileDistance

    #inertia
def missileInertia():
    if count > 500:
        missileVNew = missileV * 0.99985
        return missileVNew
    else:
        return missileV      

    #missile position direct guidance
def missilePosDirect():
    global missileX, missileY, redforX, redforY, bluforV, oldUX, oldUY, missileLaunchV, count
    uX = (redforX - missileX) / missileDistance
    uY = (redforY - missileY) / missileDistance
    if oldUX is None and oldUY is None:
        oldUX = uX
        oldUY = uY

    dUX = uX - oldUX
    dUY = uY - oldUY
    if dUX > 0.005 or dUX < -0.005:
        uX = oldUX + 0.005 * (1 if dUX > 0 else -1)
    if dUY > 0.005 or dUY < -0.005:
        uY = oldUY + 0.005 * (1 if dUY > 0 else -1)
    if count < 500:
        launchDelta = missileV - bluforV
        if missileLaunchV is None:
            missileLaunchV = bluforV
            uX = 1
            uY = 0
        missileLaunchV = missileLaunchV + (launchDelta * 0.002)
        missileX = missileX + (missileLaunchV * uX * 0.01)
        missileY = missileY + (missileLaunchV * uY * 0.01)
    
    else:
        missileX = missileX + (missileV * uX * 0.01)
        missileY = missileY + (missileV * uY * 0.01)
    oldUX = uX
    oldUY = uY
    missileXY = [missileX, missileY, oldUX, oldUY]
    return missileXY

    #missile position lead guidance
def missilePosLead():
    global missileX, missileY, redforX, redforY, bluforV, oldUX, oldUY, missileLaunchV, count, redforLeadX, launchTime
    leadCalc()
    uX = (redforLeadX - missileX) / missileDistance
    uY = (redforY - missileY) / missileDistance
    if oldUX is None and oldUY is None:
        oldUX = uX
        oldUY = uY

    dUX = uX - oldUX
    dUY = uY - oldUY
    if dUX > 0.001 or dUX < -0.001:
        uX = oldUX + 0.001 * (1 if dUX > 0 else -1)
    if dUY > 0.001 or dUY < -0.001:
        uY = oldUY + 0.001 * (1 if dUY > 0 else -1)
    if count < 500:
        launchDelta = missileV - bluforV
        if missileLaunchV is None:
            missileLaunchV = bluforV
            uX = 1
            uY = 0
        missileLaunchV = missileLaunchV + (launchDelta * 0.002)
        missileX = missileX + (missileLaunchV * uX * 0.01)
        missileY = missileY + (missileLaunchV * uY * 0.01)
    
    else:
        missileX = missileX + (missileV * uX * 0.01)
        missileY = missileY + (missileV * uY * 0.01)
    oldUX = uX
    oldUY = uY
    missileXY = [missileX, missileY, oldUX, oldUY]
    launchTime += 1
    return missileXY

    #leadCalc
def leadCalc():
    global redforX, redforY, missileV, missileX, missileY, redforLeadX, launchTime, timeToTarget
    dx = redforX - missileX
    dy = redforY - missileY
    timeToTarget = math.hypot(dx, dy) / missileV
    redforLeadX = redforX - (redforV * timeToTarget)
    return redforLeadX
    #plotting
count = 0
x = np.array([bluforXInit])
y = np.array([bluforYInit])
redX = np.array([redforXInit])
redY = np.array([redforYInit])
bluX = np.array([bluforXInit])
bluY = np.array([bluforYInit])

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
    redforX = redforX - (redforV * 0.01)
    missileXY = missilePosLead()
    missileX = missileXY[0]
    missileY = missileXY[1]

    missileDistance = missileCalc()
    bluforX = bluforX + (bluforV * 0.01)

    if oldMissileDistance < missileDistance:
        lockBreakCount += 1
        if lockBreakCount > 100:
            print("Missile has lost lock")
            lostLock = 1
            break
    oldMissileDistance = missileDistance
    if count % 10 == 0:
        print(f"{count/100} S"
              f"\n\n{missileX:8.1f} m downrange\n"
              f"{missileY:8.1f} m altitude\n"
              f"{missileDistance:8.1f} m from target\n"
              f"{missileV:8.1f} m/s"
              f"{(timeToTarget):8.1f} s"
              f"{(launchTime/100):8.1f} s")
    if count % 10 == 0:
        x = np.append(x, missileX)
        y = np.append(y, missileY)
        redX = np.append(redX, redforX)
        redY = np.append(redY, redforY)
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
if lostLock == 0:
    print("Missile has proxy fused")
try:
    print(time, "seconds of flight time")
except:
    print("Flight time could not be calculated.")
plt.ioff()
plt.show()
