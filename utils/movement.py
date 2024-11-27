import time
import math
from statistics import mean

from . import statics
from brickUtils import brick
from brickUtils.brick import BP, EV3UltrasonicSensor, Motor, TouchSensor, wait_ready_sensors
from utils import colour
from utils import obstacle

def wait_for_motor(motor):
    # Wait for motor to spin or slow down
    while math.isclose(motor.get_speed(), 0):
        time.sleep(statics.MotorPollDelay)
    while not math.isclose(motor.get_speed(), 0):
        time.sleep(statics.MotorPollDelay)

def init_motor(motor):
        motor.reset_encoder()
        motor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
        motor.set_power(0)

def moveForwardUntilObstacle(leftMotor, rightMotor, frontUS, sideUS, leftCS, rightCS, navMap):
    #Get distance to wall before anything starts
    referenceDistance = sideUS.get_value()
    while referenceDistance == None:
        print(referenceDistance)
        time.sleep(0.3)
        referenceDistance = sideUS.get_value()
    
    #Initial encoder, for marking path as visited later on map
    initialLeft, initialRight = leftMotor.get_encoder(), rightMotor.get_encoder()
    
    #Obstacle being tracked
    targetObstacle = None
    
    #Start moving
    leftMotor.set_dps(statics.CruisingSpeed)
    rightMotor.set_dps(statics.CruisingSpeed)
    while True:
        keepStraight(leftMotor, rightMotor, sideUS, referenceDistance)

        objectL = colour.getObject(rightCS.get_value())
        objectR = colour.getObject(leftCS.get_value())
        
        #Colour sensor sees cube / poop / water, refactor into another function when possible? # of passed vars w/ motors?
        if isinstance(objectL, statics.CubeColours):
            if objectL.isPoop():
                print("Left CS: shit")
                stopMotors(leftMotor, rightMotor)
                pickupLeft(leftMotor, rightMotor)
                return
            else:
                print("Left CS obstacle cube")
                stopMotors(leftMotor, rightMotor)
                currentCoords = navMap.MarkVisitedPath(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
                navMap.MarkObstacle(statics.LeftColourSensorLocation, None, currentCoords)
                return
        elif isinstance(objectL, statics.GroundColours.WATER):
            print("Left CS water")
            stopMotors(leftMotor, rightMotor)
            currentCoords = navMap.MarkVisitedPath(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
            navMap.MarkWater(statics.LeftColourSensorLocation, None, currentCoords)
            return
        
        #Same thing, for right side CS
        if isinstance(objectR, statics.CubeColours):
            if objectR.isPoop():
                print("Right CS: shit")
                stopMotors(leftMotor, rightMotor)
                pickupLeft(leftMotor, rightMotor)
                return
            else:
                print("Right CS obstacle cube")
                stopMotors(leftMotor, rightMotor)
                currentCoords = navMap.MarkVisitedPath(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
                navMap.MarkObstacle(statics.RightColourSensorLocation, None, currentCoords)
                return
        elif isinstance(objectR, statics.GroundColours.WATER):
            print("Right CS water")
            stopMotors(leftMotor, rightMotor)
            currentCoords = navMap.MarkVisitedPath(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
            navMap.MarkWater(statics.RightColourSensorLocation, None, currentCoords)
            return

        # Track obstacle in front, if close enough
        frontDistance = frontUS.get_value()
        if targetObstacle == None:
            if frontDistance < statics.TrackingThreshold:
                targetObstacle = [frontDistance, leftMotor.get_encoder(), rightMotor.get_encoder()]
                print("init " + str(targetObstacle))
        else:
            if frontDistance < statics.PickupThreshold:
                print("Stopped at measured: " + str(frontDistance))
                stopMotors(leftMotor, rightMotor)
                print(obstacle.getObstacleColour(leftMotor, rightMotor, leftCS, rightCS)) #test
                break
            elif frontDistance < statics.TrackingThreshold:
                targetObstacle = [frontDistance, leftMotor.get_encoder(), rightMotor.get_encoder()]
                print(targetObstacle) #DEBUG
            else:
                theoreticalDistance = getObstacleDistance(targetObstacle, leftMotor.get_encoder(), rightMotor.get_encoder())
                print("theory " + str(theoreticalDistance))
                if theoreticalDistance < statics.PickupThreshold:
                    print("Stopped at theoretical: " + str(theoreticalDistance))
                    stopMotors(leftMotor, rightMotor)
                    print(obstacle.getObstacleColour(leftMotor, rightMotor, leftCS, rightCS)) #test
                    break
                    #function
        time.sleep(0.3)

def keepStraight(leftMotor, rightMotor, sideUS, referenceDistance):
    distanceToWall = sideUS.get_value()
    if (referenceDistance - distanceToWall) < -statics.DeviationLimit:
        print("Veering left")
        motorSpeedCorrection(leftMotor)
    elif (referenceDistance - distanceToWall) > statics.DeviationLimit:
        print("Veering right")
        motorSpeedCorrection(rightMotor)

def motorSpeedCorrection(motor):
    motor.set_dps(statics.SpeedCorrectionFactor * statics.CruisingSpeed)
    time.sleep(1)
    motor.set_dps(statics.CruisingSpeed)
    
def pickupLeft(leftMotor, rightMotor):
    return

def pickupRight(leftMotor, rightMotor):
    return
    
def getObstacleDistance(targetObstacle, leftEncoder, rightEncoder):
    return targetObstacle[0] - abs(mean([leftEncoder - targetObstacle[1], rightEncoder - targetObstacle[2]]) / 360) * statics.WheelCircumference

def rotateLeft90(LeftMotor, RightMotor):
    #Values to play with: multiplying powerlimit by some factor, same for the result of angleToMotorRotation (currently 1.42)
    RightMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
    LeftMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
    
    RightMotor.set_position_relative(1.42 * angleToMotorRotation(90, statics.WheelBase, statics.WheelRadius))
    LeftMotor.set_position_relative(-1.42 * angleToMotorRotation(90, statics.WheelBase, statics.WheelRadius))

def rotateRight90(LeftMotor, RightMotor):
    #Play with the same values as rotateLeft90, if cant move back into place, make the function rotateRight45, and we'll
    #encapsulate this function under another rotateRight90
    RightMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
    LeftMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
    
    RightMotor.set_position_relative(-1.42 * angleToMotorRotation(90, statics.WheelBase, statics.WheelRadius))
    LeftMotor.set_position_relative(1.42 * angleToMotorRotation(90, statics.WheelBase, statics.WheelRadius))

def rotateLeft10(LeftMotor, RightMotor):
    #Use the same code as rotate90, just make angleToMotorRotation 10 or appropriate small angle, rename function accordingly
    return

def rotateRight10(LeftMotor, RightMotor):
    #Use the same code as rotate90, just make angleToMotorRotation 10 or appropriate small angle, rename function accordingly
    return

def angleToMotorRotation(angle, wheelBase, wheelRadius):
    angleInRadians = angle * math.pi / 180
    distanceTravelled = angleInRadians * wheelBase
    return 360 * (distanceTravelled / (2 * math.pi * wheelRadius)) / 2 * 0.95

def stopMotors(leftMotor, rightMotor):
    leftMotor.set_dps(0)
    rightMotor.set_dps(0)