import time
import math
from statistics import mean

from . import statics
from brickUtils import brick
from brickUtils.brick import BP, EV3UltrasonicSensor, Motor, TouchSensor, wait_ready_sensors
from utils import colour
from utils import obstacle
from modules import crane

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
    
def moveForwardFallback(leftMotor, rightMotor, armMotor, clawMotor, frontUS, sideUS, leftCS, rightCS, distanceToTravel):
    if distanceToTravel == None:
        distanceToTravel = 50
    referenceDistance = sideUS.get_value()
    referenceFront = frontUS.get_value()
    while referenceDistance == None or frontUS.get_value() == None:
        time.sleep(0.3)
        referenceDistance = sideUS.get_value()
        referenceFront = frontUS.get_value()
    print("Reference Side: " + str(referenceDistance))
    print("Reference Front: " + str(referenceFront))
    
    initialLeft, initialRight = leftMotor.get_encoder(), rightMotor.get_encoder()

    while getDistance(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder()) < distanceToTravel:
        leftMotor.set_dps(statics.CruisingSpeed)
        rightMotor.set_dps(statics.CruisingSpeed)
        #keepStraight(leftMotor, rightMotor, sideUS, referenceDistance)
        
        objectL = colour.getObject(leftCS.get_value())
        objectR = colour.getObject(rightCS.get_value())
        print("LEFT: " + str(objectL))
        print("RIGHT: " + str(objectR))
        
        if isinstance(objectL, statics.CubeColours):
            readings = [objectL]
            stopMotors(leftMotor, rightMotor)
            
            rotateLeft8(leftMotor, rightMotor)
            time.sleep(0.2)
            readings.append(colour.getObject(leftCS.get_value()))
            rotateFromRightColor(leftMotor, rightMotor)
            time.sleep(0.2)
            
            rotateRight8(leftMotor, rightMotor)
            time.sleep(0.2)
            readings.append(colour.getObject(leftCS.get_value()))
            rotateFromLeftColor(leftMotor, rightMotor)
            time.sleep(0.2)
            
            if statics.CubeColours.YELLOW in readings or statics.CubeColours.ORANGE in readings:
                print("Left CS: shit")
                moveBackwards(leftMotor, rightMotor)
                pickupLeft(leftMotor, rightMotor, armMotor, clawMotor)
                continue
            else:
                print("Left CS obstacle cube")
                return getDistance(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
        elif objectL == statics.GroundColours.WATER:
            print("Left CS water")
            stopMotors(leftMotor, rightMotor)
            return getDistance(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
        
        if isinstance(objectR, statics.CubeColours):
            readings = [objectR]
            stopMotors(leftMotor, rightMotor)
            
            rotateLeft8(leftMotor, rightMotor)
            time.sleep(0.2)
            readings.append(colour.getObject(rightCS.get_value()))
            rotateFromRightColor(leftMotor, rightMotor)
            time.sleep(0.2)
            
            rotateRight8(leftMotor, rightMotor)
            time.sleep(0.2)
            readings.append(colour.getObject(rightCS.get_value()))
            rotateFromLeftColor(leftMotor, rightMotor)
            time.sleep(0.2)

            if statics.CubeColours.YELLOW in readings or statics.CubeColours.ORANGE in readings:
                print("Right CS: shit")
                moveBackwards(leftMotor, rightMotor)
                pickupRight(leftMotor, rightMotor, armMotor, clawMotor)
                continue
            else:
                print("Right CS obstacle cube")
                return getDistance(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
        elif objectR == statics.GroundColours.WATER:
            print("Right CS water")
            stopMotors(leftMotor, rightMotor)
            return getDistance(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
        
        distanceToFloor = frontUS.get_value()
        print(distanceToFloor)
        if abs(referenceFront - frontUS.get_value()) > 0.6:
            stopMotors(leftMotor, rightMotor)
            cube = obstacle.getObstacleColour(leftMotor, rightMotor, leftCS, rightCS)
            if cube == None:
                print("Failed to find cube with CS")
                return getDistance(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
            if cube == statics.CubeColours.ORANGE or cube == statics.CubeColours.YELLOW:
                crane.pickup(armMotor, clawMotor)
                leftMotor.set_dps(statics.CruisingSpeed)
                rightMotor.set_dps(statics.CruisingSpeed)
            else:
                return getDistance(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
        time.sleep(0.1)

    return getDistance(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())

def moveForwardUntilObstacle(leftMotor, rightMotor, armMotor, clawMotor, frontUS, sideUS, leftCS, rightCS, distance, navMap):
    if distance == None:
        distance = math.inf
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
    while getTravelledDistance(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder()) <= distance:
        keepStraight(leftMotor, rightMotor, sideUS, referenceDistance)

        objectL = colour.getObject(leftCS.get_value())
        objectR = colour.getObject(rightCS.get_value())
        
        #Colour sensor sees cube / poop / water, refactor into another function when possible? # of passed vars w/ motors?
        if isinstance(objectL, statics.CubeColours):
            if objectL == statics.CubeColours.YELLOW or objectL == statics.CubeColours.ORANGE:
                print("Left CS: shit")
                stopMotors(leftMotor, rightMotor)
                pickupLeft(leftMotor, rightMotor, armMotor, clawMotor)
                return
            else:
                print("Left CS obstacle cube")
                stopMotors(leftMotor, rightMotor)
                #currentCoords = navMap.MarkVisitedPath(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
                #navMap.MarkObstacle(statics.LeftColourSensorLocation, None, currentCoords)
                return getDistance(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
        elif objectL == statics.GroundColours.WATER:
            print("Left CS water")
            stopMotors(leftMotor, rightMotor)
            #currentCoords = navMap.MarkVisitedPath(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
            #navMap.MarkWater(statics.LeftColourSensorLocation, None, currentCoords)
            return getDistance(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
        
        #Same thing, for right side CS
        if isinstance(objectR, statics.CubeColours):
            if objectR == statics.CubeColours.YELLOW or objectR == statics.CubeColours.ORANGE:
                print("Right CS: shit")
                stopMotors(leftMotor, rightMotor)
                pickupLeft(leftMotor, rightMotor, armMotor, clawMotor)
                return
            else:
                print("Right CS obstacle cube")
                stopMotors(leftMotor, rightMotor)
                #currentCoords = navMap.MarkVisitedPath(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
                navMap.MarkObstacle(statics.RightColourSensorLocation, None, currentCoords)
                return getDistance(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
        elif objectR == statics.GroundColours.WATER:
            print("Right CS water")
            stopMotors(leftMotor, rightMotor)
            currentCoords = navMap.MarkVisitedPath(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder(), [6, 10])
            #navMap.MarkWater(statics.RightColourSensorLocation, None, currentCoords)
            return getDistance(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())

        # Track obstacle in front, if close enough
        frontDistance = frontUS.get_value()
        print("front distance: " + str(frontDistance))
        if targetObstacle == None:
            if frontDistance < statics.TrackingThreshold:
                targetObstacle = [frontDistance, leftMotor.get_encoder(), rightMotor.get_encoder()]
                print("init " + str(targetObstacle))
        else:
            if frontDistance < statics.PickupThreshold:
                print("Stopped at measured: " + str(frontDistance))
                stopMotors(leftMotor, rightMotor)
                cube = obstacle.getObstacleColour(leftMotor, rightMotor, leftCS, rightCS)
                print(cube)
                if cube == statics.CubeColours.YELLOW or cube == statics.CubeColours.ORANGE:
                    crane.pickup(armMotor, clawMotor)
                break
            elif frontDistance < statics.TrackingThreshold:
                targetObstacle = [frontDistance, leftMotor.get_encoder(), rightMotor.get_encoder()]
                print(targetObstacle) #DEBUG
            else:
                theoreticalDistance = getObstacleDistance(targetObstacle, leftMotor.get_encoder(), rightMotor.get_encoder())
                print("theory " + str(theoreticalDistance))
                if theoreticalDistance < statics.TheoryPickupThreshold:
                    print("Stopped at theoretical: " + str(theoreticalDistance))
                    stopMotors(leftMotor, rightMotor)
                    cube = obstacle.getObstacleColour(leftMotor, rightMotor, leftCS, rightCS)
                    print(cube)
                    if cube == statics.CubeColours.YELLOW or cube == statics.CubeColours.ORANGE:
                        crane.pickup(armMotor, clawMotor)
                    break
                    #function
        time.sleep(0.1)

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
    time.sleep(statics.CorrectionTimer)
    motor.set_dps(statics.CruisingSpeed)
    
def pickupLeft(leftMotor, rightMotor, armMotor, clawMotor):
    for _ in range(8):
        rotateFromLeftColor(leftMotor, rightMotor)
        time.sleep(0.5)
    moveBackwards(leftMotor, rightMotor)
    crane.pickup(armMotor, clawMotor)
    time.sleep(0.5)
    for _ in range(6):
        rotateRight8(leftMotor, rightMotor)
        time.sleep(0.5)
    time.sleep(1)
    return

def pickupRight(leftMotor, rightMotor, armMotor, clawMotor):
    for i in range(8):
        rotateFromRightColor(leftMotor, rightMotor)
        time.sleep(0.5)
    moveBackwards(leftMotor, rightMotor)
    time.sleep(1)
    crane.pickup(armMotor, clawMotor)
    time.sleep(0.5)
    for i in range(6):
        rotateLeft8(leftMotor, rightMotor)
        time.sleep(0.5)
    return

def getTravelledDistance(initLeft, initRight, leftEncoder, rightEncoder):
    return abs(mean([leftEncoder - initLeft, rightEncoder - initRight]) / 360) * statics.WheelCircumference

def getObstacleDistance(targetObstacle, leftEncoder, rightEncoder):
    return targetObstacle[0] - abs(mean([leftEncoder - targetObstacle[1], rightEncoder - targetObstacle[2]]) / 360) * statics.WheelCircumference

def rotateLeft90(LeftMotor, RightMotor):
    #Values to play with: multiplying powerlimit by some factor, same for the result of angleToMotorRotation (currently 1.42)
    RightMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
    LeftMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
    
    RightMotor.set_position_relative(-0.95 * angleToMotorRotation(90, statics.WheelBase, statics.WheelRadius))
    LeftMotor.set_position_relative(0.95 * angleToMotorRotation(90, statics.WheelBase, statics.WheelRadius))

def rotateRight90(LeftMotor, RightMotor):
    #Play with the same values as rotateLeft90, if cant move back into place, make the function rotateRight45, and we'll
    #encapsulate this function under another rotateRight90
    RightMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
    LeftMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
    
    RightMotor.set_position_relative(1.05 * angleToMotorRotation(90, statics.WheelBase, statics.WheelRadius))
    LeftMotor.set_position_relative(-1.05 * angleToMotorRotation(90, statics.WheelBase, statics.WheelRadius))

def rotateLeft8(LeftMotor, RightMotor):
    #Use the same code as rotate90, just make angleToMotorRotation 10 or appropriate small angle, rename function accordingly
    RightMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
    LeftMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
    
    RightMotor.set_position_relative(-1 * angleToMotorRotation(8, statics.WheelBase, statics.WheelRadius))
    LeftMotor.set_position_relative(1 * angleToMotorRotation(8, statics.WheelBase, statics.WheelRadius))

def rotateRight8(LeftMotor, RightMotor):
    #Use the same code as rotate90, just make angleToMotorRotation 10 or appropriate small angle, rename function accordingly
    RightMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
    LeftMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
    
    RightMotor.set_position_relative(1 * angleToMotorRotation(8, statics.WheelBase, statics.WheelRadius))
    LeftMotor.set_position_relative(-1 * angleToMotorRotation(8, statics.WheelBase, statics.WheelRadius))

def rotateFromLeftColor(LeftMotor, RightMotor):
    RightMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
    LeftMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
    
    RightMotor.set_position_relative(-0.95 * angleToMotorRotation(8, statics.WheelBase, statics.WheelRadius))
    LeftMotor.set_position_relative(0.95 * angleToMotorRotation(8, statics.WheelBase, statics.WheelRadius))

def rotateFromRightColor(LeftMotor, RightMotor):
    RightMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
    LeftMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
    
    RightMotor.set_position_relative(1 * angleToMotorRotation(8, statics.WheelBase, statics.WheelRadius))
    LeftMotor.set_position_relative(-1 * angleToMotorRotation(8, statics.WheelBase, statics.WheelRadius))

def angleToMotorRotation(angle, wheelBase, wheelRadius):
    angleInRadians = angle * math.pi / 180
    distanceTravelled = angleInRadians * wheelBase
    return 360 * (distanceTravelled / (2 * math.pi * wheelRadius))

def stopMotors(LeftMotor, RightMotor):
    LeftMotor.set_dps(0)
    RightMotor.set_dps(0)
    
def moveBackwards(LeftMotor, RightMotor):
    RightMotor.set_limits(statics.MotorPowerLimit, -statics.MotorSpeedLimit)
    LeftMotor.set_limits(statics.MotorPowerLimit, -statics.MotorSpeedLimit)

    RightMotor.set_dps(-statics.CruisingSpeed)
    LeftMotor.set_dps(-statics.CruisingSpeed)
    time.sleep(0.6)
    stopMotors(LeftMotor, RightMotor)
    
def fuckedupmoveback(leftMotor, rightMotor, distance):
    initLeft, initRight = leftMotor.get_encoder(), rightMotor.get_encoder()
    print("moving back")
    rightMotor.set_limits(statics.MotorPowerLimit, -statics.MotorSpeedLimit)
    leftMotor.set_limits(statics.MotorPowerLimit, -statics.MotorSpeedLimit)

    rightMotor.set_dps(-statics.CruisingSpeed)
    leftMotor.set_dps(-statics.CruisingSpeed)
    
    while getDistance(initLeft, initRight, leftMotor.get_encoder(), rightMotor.get_encoder()) < distance:
        continue
    stopMotors(leftMotor, rightMotor)
    
def getDistance(initLeft, initRight, finalLeft, finalRight):
    return abs(mean([finalLeft - initLeft, finalRight - initRight])) / 360 * statics.WheelCircumference