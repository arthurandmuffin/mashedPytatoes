from time import sleep

from . import statics
from . import movement
from . import colour

def obstacleCloserThan(usSensor, distance):
    return usSensor.get_value()

def colourSensorObstacles():
    return

def getObstacleColour(leftMotor, rightMotor, leftCS, rightCS):
    movement.rotateLeft(leftMotor, rightMotor, -15, 30, 30)
    sleep(0.3)
    if isinstance(colour.getObject(rightCS.get_value()), statics.CubeColours):
        movement.rotateRight(leftMotor, rightMotor, -15, 30, 30)
        sleep(0.3)
        return colour.getObject(rightCS.get_value())
    
    movement.rotateLeft(leftMotor, rightMotor, 15, 30, 30)
    sleep(0.3)
    if isinstance(colour.getObject(rightCS.get_value()), statics.CubeColours):
        movement.rotateRight(leftMotor, rightMotor, -30, 30, 30)
        sleep(0.3)
        return colour.getObject(rightCS.get_value())
    
    movement.rotateLeft(leftMotor, rightMotor, 15, 30, 30)
    sleep(0.3)
    if isinstance(colour.getObject(rightCS.get_value()), statics.CubeColours):
        movement.rotateRight(leftMotor, rightMotor, -45, 30, 30)
        sleep(0.3)
        return colour.getObject(rightCS.get_value())
    
    return "fucked"