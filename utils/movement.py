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

    # Account for distance between colour sensors and robot
    nearWaterL = 0
    nearWaterR = 0

    while True:
        keepStraight(leftMotor, rightMotor, sideUS, referenceDistance)

        # COLOUR SENSOR
        colourL = colour.getColour(leftCS.get_value())
        colourR = colour.getColour(rightCS.get_value())

        # LEFT
        # Left colour sensor detects an OBJECT
        if colourL and colourL in statics.CubeColours:

            # Object is POOP
            if (colourL == statics.CubeColours.YELLOW) or (colourL == statics.CubeColours.ORANGE):
                print("Left CS: shit")
                stopMotors(leftMotor, rightMotor)
                pickupLeft(leftMotor, rightMotor)
                return

            # Object is OBSTACLE
            else:
                print("Left CS obstacle cube")
                stopMotors(leftMotor, rightMotor)
                #                 currentCoords = navMap.MarkVisitedPath(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
                #                 navMap.MarkObstacle(statics.LeftColourSensorLocation, None, currentCoords)
                return

        # Left colour sensor detects WATER
        elif colourL == statics.GroundColours.WATER:
            nearWaterL += 1
            print("Left CS water " + str(nearWaterL))
            #             currentCoords = navMap.MarkVisitedPath(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
            #             navMap.MarkWater(statics.LeftColourSensorLocation, None, currentCoords)
            if nearWaterL == 5:
                stopMotors(leftMotor, rightMotor)
                moveBackwards(leftMotor, rightMotor)
                rotateRight8(leftMotor, rightMotor)
                if colourL != statics.GroundColours.WATER:
                    rotateLeft8(leftMotor, rightMotor)
                    nearWaterL = -5
                    continue
                else:
                    moveBackwards(leftMotor, rightMotor)
                    rotateRight8(leftMotor, rightMotor)
                    continue
            else:
                continue

        # RIGHT
        # Right colour sensor detects an OBJECT
        if colourR and colourR in statics.CubeColours:

            # Object is POOP
            if (colourR == statics.CubeColours.YELLOW) or (colourR == statics.CubeColours.ORANGE):
                print("Right CS: shit")
                stopMotors(leftMotor, rightMotor)
                pickupRight(leftMotor, rightMotor)
                return

            # Object is OBSTACLE
            else:
                print("Right CS obstacle cube")
                stopMotors(leftMotor, rightMotor)
                #                 currentCoords = navMap.MarkVisitedPath(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
                #                 navMap.MarkObstacle(statics.RightColourSensorLocation, None, currentCoords)
                return

        # Right colour sensor detects WATER
        elif colourR == statics.GroundColours.WATER:
            nearWaterR += 1
            #         elif isinstance(colourR, statics.GroundColours.WATER):
            print("Right CS water " + str(nearWaterR))
            #             currentCoords = navMap.MarkVisitedPath(initialLeft, initialRight, leftMotor.get_encoder(), rightMotor.get_encoder())
            #             navMap.MarkWater(statics.RightColourSensorLocation, None, currentCoords)
            if nearWaterR == 5:
                stopMotors(leftMotor, rightMotor)
                moveBackwards(leftMotor, rightMotor)
                rotateLeft8(leftMotor, rightMotor)
                if colourL != statics.GroundColours.WATER:
                    rotateLeft8(leftMotor, rightMotor)
                    nearWaterR = -5
                    continue
                else:
                    moveBackwards(leftMotor, rightMotor)
                    rotateLeft8(leftMotor, rightMotor)
                    continue
            else:
                continue

        # FRONT US-SENSOR
        # Track obstacle in front, if close enough
        frontDistance = frontUS.get_value()
        if targetObstacle == None:
            if frontDistance < statics.TrackingThreshold:  # Right now 20
                #                 print(str(frontDistance) + " < " + str(statics.TrackingTreshold))
                targetObstacle = [frontDistance, leftMotor.get_encoder(), rightMotor.get_encoder()]
                print("init " + str(targetObstacle) + " --> target obstacle in sight")
        else:
            print("targetObstacle is not None")

            # Distance between robot and cube is less than 6
            if frontDistance < statics.PickupThreshold:  # Right now 6
                print("Stopped at measured: " + str(frontDistance))
                stopMotors(leftMotor, rightMotor)
                objectColour = obstacle.getObstacleColour(leftMotor, rightMotor, leftCS, rightCS)
                print(objectColour)
                if (objectColour == statics.CubeColours.YELLOW) or (objectColour == statics.CubeColours.ORANGE):
                    crane.pickup(armMotor, clawMotor, leftMotor, rightMotor)
                break

            # Distance between robot and cube is between 6 and 20, so we're approaching it
            elif frontDistance < statics.TrackingThreshold:
                targetObstacle = [frontDistance, leftMotor.get_encoder(), rightMotor.get_encoder()]
                print("Approaching target: " + str(targetObstacle))  # DEBUG

            else:
                theoreticalDistance = getObstacleDistance(targetObstacle, leftMotor.get_encoder(),
                                                          rightMotor.get_encoder())
                print("theory " + str(theoreticalDistance))
                if theoreticalDistance < statics.PickupThreshold:
                    print("Stopped at theoretical: " + str(theoreticalDistance))
                    stopMotors(leftMotor, rightMotor)
                    print(obstacle.getObstacleColour(leftMotor, rightMotor, leftCS, rightCS))  # test
                    break
                    # function

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
    time.sleep(statics.CorrectionTimer)
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
    
def moveBackwardToPickup(LeftMotor, RightMotor):
    RightMotor.set_limits(statics.MotorPowerLimit, -statics.MotorSpeedLimit)
    LeftMotor.set_limits(statics.MotorPowerLimit, -statics.MotorSpeedLimit)

    RightMotor.set_dps(-statics.CruisingSpeed)
    # time.sleep(0.5)
    LeftMotor.set_dps(-statics.CruisingSpeed)
    time.sleep(0.6)
    stopMotors(LeftMotor, RightMotor)