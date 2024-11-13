import time
import math
from . import statics
from utils import brick
from utils import BP, EV3UltrasonicSensor, Motor, TouchSensor, wait_ready_sensors
from BrickPi import *

def wait_for_motor(Motor):
    # Wait for motor to spin or slow down
    while math.isclose(motor.get_speed(), 0):
        time.sleep(statics.MotorPollDelay)
    while not math.isclose(motor.get_speed, 0):
        time.sleep(statics.MotorPollDelay)

def init_motor(Motor):
        motor.reset_encoder()
        motor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
        motor.set_power(0)

def moveForward(distance, speed):
    LEFT_MOTOR.set_dps(speed)
    RIGHT_MOTOR.set_dps(speed)

    LEFT_MOTOR.set_limits(statics.MotorPowerLimit, speed)
    RIGHT_MOTOR.set_limits(statics.MotorPowerLimit, speed)

    LEFT_MOTOR.set_position_relative(int(distance*statics.DistToDeg))
    RIGHT_MOTOR.set_position_relative(int(distance*statics.DistToDeg))

    wait_for_motor(RIGHT_MOTOR)


def moveForwardUntilObstacle():
    while US_SENSOR.get_distance() > 0.1:
        time.sleep(statics.MotorPollDelay)
    
    stopMotors()

def moveBackward(distance, speed):
     LEFT_MOTOR.set_dps(speed)
     RIGHT_MOTOR.set_dps(speed)

     LEFT_MOTOR.set_limits(statics.MotorPowerLimit, speed)
     RIGHT_MOTOR.set_limits(statics.MotorPowerLimit, speed)

     LEFT_MOTOR.set_position_relative(-int(distance*statics.DistToDeg))
     RIGHT_MOTOR.set_position_relative(-int(distance*statics.DistToDeg))

     wait_for_motor(RIGHT_MOTOR)
          
          

def rotate(angle):
    LEFT_MOTOR.set_limits(statics.MotorPowerLimit, statics.MotorTurnSpeed)
    RIGHT_MOTOR.set_limits(statics.MotorPowerLimit, statics.MotorTurnSpeed)

    LEFT_MOTOR.set_position_relative(-int(angle * statics.OrientToDeg))
    RIGHT_MOTOR.set_position_relative(int(angle * statics.OrientToDeg))
    wait_for_motor(RIGHT_MOTOR)

def stopMotors():
    LEFT_MOTOR.set_dps(0)
    RIGHT_MOTOR.set_dps(0)

def turnLeft(angle=90):
    rotate(angle)

def turnRight(angle=90):
    rotate(-angle)



