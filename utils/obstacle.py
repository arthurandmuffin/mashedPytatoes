from time import sleep

from . import statics
from . import movement
from . import colour

def obstacleCloserThan(usSensor, distance):
    return usSensor.get_value()

def colourSensorObstacles():
    return

def getObstacleColour(leftMotor, rightMotor, leftCS, rightCS):
    count = 0
    for i in range(8):
        movement.rotateLeft8(leftMotor, rightMotor)
        sleep(1)
        rightRGB = rightCS.get_value()
        print(rightRGB)
        rightCSReading = colour.getObject(rightRGB)
        if isinstance(rightCSReading, statics.CubeColours):
            count += 1
            if count > 1:
                for _ in range(i):
                    movement.rotateFromRightColor(leftMotor, rightMotor)
                    sleep(0.5)
                movement.moveBackwards(leftMotor, rightMotor)
                sleep(1.2)
                return rightCSReading

    for i in range(8):
        movement.rotateFromRightColor(leftMotor, rightMotor)
        sleep(1)
    movement.moveBackwards(leftMotor, rightMotor)
    count = 0
    for k in range(8):
        movement.rotateRight8(leftMotor, rightMotor)
        sleep(1)
        leftRGB = leftCS.get_value()
        print(leftRGB)
        leftCSReading = colour.getObject(leftRGB)
        if isinstance(leftCSReading, statics.CubeColours):
            count += 1
            if count > 1:
                for _ in range(k):
                    movement.rotateFromLeftColor(leftMotor, rightMotor)
                    sleep(0.5)
                movement.moveBackwardToPickup(leftMotor, rightMotor)
                sleep(1.2)
                return leftCSReading
        
    movement.moveBackwardToPickup(leftMotor, rightMotor)
    sleep(1.2)
    for k in range(8):
        movement.rotateFromLeftColor(leftMotor, rightMotor)
        sleep(1)
    movement.moveBackwards(leftMotor, rightMotor)
    return None