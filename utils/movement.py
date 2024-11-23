import time
import math
from . import statics
from brickUtils import brick
from brickUtils.brick import BP, EV3UltrasonicSensor, Motor, TouchSensor, wait_ready_sensors
from utils import colour

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

def moveForward(distance, speed):
    LEFT_MOTOR.set_dps(speed)
    RIGHT_MOTOR.set_dps(speed)

    LEFT_MOTOR.set_position_relative(int(distance*statics.DistToDeg))
    RIGHT_MOTOR.set_position_relative(int(distance*statics.DistToDeg))

    wait_for_motor(RIGHT_MOTOR)

def moveForwardUntilObstacle(leftMotor, rightMotor, frontUS, sideUS, leftCS, rightCS):
    referenceDistance = sideUS.get_value() + 5 # added padding
    print("got reference distance: " + str(referenceDistance))
    initialLeft, initialRight = leftMotor.get_encoder(), rightMotor.get_encoder()

    while True:
        leftMotor.set_dps(statics.CruisingSpeed)
        rightMotor.set_dps(statics.CruisingSpeed)
        
        frontDistance = frontUS.get_value() + 5 #padding
        sideDistance = sideUS.get_value()
        
        # Self-correct position based on wall distance
        if (referenceDistance - sideDistance) < -statics.DeviationLimit:
            print("left motor speed up")
            motorSpeedCorrection(leftMotor)
        elif (referenceDistance - sideDistance) > statics.DeviationLimit:
            motorSpeedCorrection(rightMotor)
            print("right motor speed up")
        
        # Stops because approaching something.
        if frontDistance < 15 or sideDistance < 15:
            stopMotors(leftMotor, rightMotor)
            time.sleep(0.5)
            moveBackward(leftMotor, rightMotor, 5, 100)
            time.sleep(1)
            rotateLeft(30, leftMotor, rightMotor, 0)
            time.sleep(1)

            if isCube:
                findAndApproachCube(leftMotor, rightMotor, leftCS, rightCS)

        colourLeft = leftCS.get_value()
        colourRight = rightCS.get_value()
        objectL = colour.getObject(colourLeft)
        objectR = colour.getObject(colourRight)
        
        if not objectL == None:
            print("ObjectL: " + objectL)
        if not objectR == None:
            print("ObjectR: " + objectR)

        if objectL == "Water" or objectR == "Water":
            stopMotors(leftMotor, rightMotor)
            moveBackward(leftMotor, rightMotor, 5, 100)
            time.sleep(2)
            if objectL == "Water":
                rotateRight(20, leftMotor, rightMotor, 0)
                time.sleep(0.5)
            else:
                rotateLeft(20, leftMotor, rightMotor, 0)
        time.sleep(0.3)

def motorSpeedCorrection(motor):
    motor.set_dps(statics.SpeedCorrectionFactor * statics.CruisingSpeed)
    time.sleep(1)
    motor.set_dps(statics.CruisingSpeed)
    

def moveBackward(leftMotor, rightMotor, distance, speed):
     leftMotor.set_dps(speed)
     rightMotor.set_dps(speed)

     leftMotor.set_position_relative(int(distance*statics.DistToDeg))
     rightMotor.set_position_relative(int(distance*statics.DistToDeg))

def rotateLeft(angleOfRotation, leftMotor, rightMotor, initialAngle):
    rightMotor.set_limits(statics.MotorPowerLimit, 200)
    leftMotor.set_limits(statics.MotorPowerLimit, 200)
    
    rightMotor.set_position_relative(-1*angleToMotorRotation(angleOfRotation, statics.WheelBase, statics.WheelRadius))
    leftMotor.set_position_relative(1*angleToMotorRotation(angleOfRotation, statics.WheelBase, statics.WheelRadius))
    
    return (initialAngle + angleOfRotation) % 360

def rotateRight(angleOfRotation, leftMotor, rightMotor, initialAngle):
    rightMotor.set_limits(1.3*statics.MotorPowerLimit, 200)
    leftMotor.set_limits(statics.MotorPowerLimit, 200)
    
    rightMotor.set_position_relative(1.2*angleToMotorRotation(angleOfRotation, statics.WheelBase, statics.WheelRadius))
    leftMotor.set_position_relative(-1.2*angleToMotorRotation(angleOfRotation, statics.WheelBase, statics.WheelRadius))
    
    return (initialAngle + angleOfRotation) % 360

def angleToMotorRotation(angle, wheelBase, wheelRadius):
    angleInRadians = angle * math.pi / 180
    distanceTravelled = angleInRadians * wheelBase
    return 360 * (distanceTravelled / (2 * math.pi * wheelRadius)) * 1

def stopMotors(leftMotor, rightMotor):
    leftMotor.set_dps(0)
    rightMotor.set_dps(0)

# To determine if it's wall or cube
def verifyCube(leftMotor, rightMotor, frontUS):
    distFront = frontUS.get_value()
    time.sleep(0.5)
    
    rotateLeft(20, leftMotor, rightMotor, 0)
    time.sleep(0.5)
    distL = frontUS.get_value()
    
    rotateRight(20, leftMotor, rightMotor, 0)
    time.sleep(0.5)
    
    rotateRight(20, leftMotor, rightMotor, 0)
    time.sleep(0.5)
    distR = frontUS.get_value()
    
    rotateLeft(20, leftMotor, rightMotor, 0)
    
    print("to the left: " + str(distL))
    print("front distance: " + str(distFront))
    print("to the right: " + str(distR))
    
def isCube(front, left, right):
    if (abs(front - left) > 5 or abs(front - right) > 5 or abs(left - right) > 10):
        return False
    else:
        print("Cube in sight")
        return True
    
def findAndApproachCube(leftMotor, rightMotor,leftCS, rightCS):
    print("Approaching cube")
    Found = False
    colourLeft = leftCS.get_value()
    colourRight = rightCS.get_value()
    objectL = colour.getObject(colourLeft)
    objectR = colour.getObject(colourRight)
    print("left: " + str(colourLeft) + str(objectL) + " AND right: " + str(colourRight) + str(objectR))

    while not Found:
        rotateLeft(20, leftMotor, rightMotor, 0)
        moveBackward(leftMotor, rightMotor, 3, 100)
        time.sleep(1)
        rotateRight(20, leftMotor, rightMotor,-20)

        # Probably not using the right parameter
        if colour.isPoop(colourLeft) == "isPoop":
            rotateRight(20, leftMotor, rightMotor, 0) # TODO: test the angle to be right where the crane picks up the poop
            print("Found dog poop")
            Found = True
        elif colour.isPoop(colourRight) == "isPoop":
            rotateLeft(20, leftMotor, rightMotor, 0)
            print("Found dog poop")
            Found = True

        elif colour.isPoop(colourLeft) == "isObstacle" or colour.isPoop(colourRight) == "isObstacle":
            stopMotors(leftMotor, rightMotor)
            print("This is an obstacle")

        else:
            print("What is this even")
            stopMotors(leftMotor, rightMotor)