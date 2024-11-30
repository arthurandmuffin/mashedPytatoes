from time import sleep
from . import statics
from . import movement
from . import colour


def obstacleCloserThan(usSensor, distance):
    return usSensor.get_value()

def colourSensorObstacles():
    return

def getObstacleColour(leftMotor, rightMotor, leftCS, rightCS):
    # Get right CS
    for i in range(8):
        movement.rotateLeft8(leftMotor, rightMotor)
        sleep(1)
        rightCSReading = colour.getColour(rightCS.get_value())
        if isinstance(rightCSReading, statics.CubeColours):
            for _ in range(i):
                movement.rotateFromRightColor(leftMotor, rightMotor)
                sleep(0.5)
            movement.moveBackwards(leftMotor, rightMotor)
            sleep(1.2)

            return rightCSReading

    # Get left CS
    for k in range(8):
        movement.rotateRight8(leftMotor, rightMotor)
        sleep(1)
        leftCSReading = colour.getColour(leftCS.get_value())
        if isinstance(leftCSReading, statics.CubeColours):
            for _ in range(k):
                movement.rotateFromLeftColor(leftMotor, rightMotor)
                sleep(0.5)
            movement.moveBackwards(leftMotor, rightMotor)
            sleep(1.2)

            return leftCSReading
    #         movement.moveBackwardToPickup(leftMotor, rightMotor)
    #         sleep(1.2)
    return None
