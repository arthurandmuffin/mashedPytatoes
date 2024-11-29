from time import sleep

from . import statics
from . import movement
from . import colour

def obstacleCloserThan(usSensor, distance):
    return usSensor.get_value()

def colourSensorObstacles():
    return

def getObstacleColour(leftMotor, rightMotor, leftCS, rightCS):
    for i in range(4):
        movement.rotateLeft8(leftMotor, rightMotor)
        sleep(0.5)
        rightCSReading = colour.getObject(rightCS.get_value())
        if isinstance(rightCSReading, statics.CubeColours):
            for _ in range(i):
                movement.rotateFromRightColor(leftMotor, rightMotor)
                sleep(0.5)
            movement.moveBackwardToPickup(leftMotor, rightMotor)
            sleep(1.2)
            return rightCSReading

    for k in range(4):
        movement.rotateRight8(leftMotor, rightMotor)
        sleep(0.5)
        leftCSReading = colour.getObject(leftCS.get_value())
        if isinstance(leftCSReading, statics.CubeColours):
            for _ in range(k):
                movement.rotateFromLeftColor(leftMotor, rightMotor)
                sleep(0.5)
            movement.moveBackwardToPickup(leftMotor, rightMotor)
            sleep(1.2)
            return leftCSReading
        
    movement.moveBackwardToPickup(leftMotor, rightMotor)
    sleep(1.2)
    return None