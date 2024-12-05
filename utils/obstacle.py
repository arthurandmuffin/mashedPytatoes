# Obstacle Analysis

from time import sleep

from . import statics
from . import movement
from . import colour

# Rotate the robot, attempt to view cube with colour sensor, return cube colour
def getObstacleColour(leftMotor, rightMotor, leftCS, rightCS):
    count = 0
    for i in range(7):
        movement.rotateLeft8(leftMotor, rightMotor)
        sleep(0.8)
        rightRGB = rightCS.get_value()
        print("OBS Right rgb: " + str(rightRGB))
        rightCSReading = colour.getObject(rightRGB)
        print(rightCSReading)
        if isinstance(rightCSReading, statics.CubeColours):
            count += 1
            if count > 1 or rightCSReading == statics.CubeColours.YELLOW or rightCSReading == statics.CubeColours.ORANGE:
                for _ in range(i):
                    movement.rotateFromRightColor(leftMotor, rightMotor)
                    sleep(0.7)
                movement.moveBackwards(leftMotor, rightMotor)
                return rightCSReading

    for i in range(7):
        movement.rotateFromRightColor(leftMotor, rightMotor)
        sleep(0.7)
    movement.moveBackwards(leftMotor, rightMotor)
    sleep(1)
    
    count = 0
    for k in range(8):
        movement.rotateRight8(leftMotor, rightMotor)
        sleep(0.5)
        leftRGB = leftCS.get_value()
        print("OBS Left RGB: " + str(leftRGB))
        leftCSReading = colour.getObject(leftRGB)
        print(rightCSReading)
        if isinstance(leftCSReading, statics.CubeColours):
            count += 1
            if count > 1 or leftCSReading == statics.CubeColours.YELLOW or leftCSReading == statics.CubeColours.ORANGE:
                for _ in range(k):
                    movement.rotateFromLeftColor(leftMotor, rightMotor)
                    sleep(0.5)
                movement.moveBackwards(leftMotor, rightMotor)
                return leftCSReading
        
    movement.moveBackwards(leftMotor, rightMotor)
    sleep(1.2)
    for k in range(8):
        movement.rotateFromLeftColor(leftMotor, rightMotor)
        sleep(0.5)
    movement.moveBackwards(leftMotor, rightMotor)
    sleep(1)
    return None