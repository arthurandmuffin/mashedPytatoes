import time
import math
from utils import brick
from utils import BP, EV3UltrasonicSensor, Motor, TouchSensor, wait_ready_sensors
from BrickPi import *

# set up
MOTOR_POLL_DELAY = 0.05
US_SENSOR = EV3UltrasonicSensor(2) 
LEFT_MOTOR = Motor("A")
RIGHT_MOTOR = Motor("D")

POWER_LIMIT = 80
SPEED_LIMIT = 270
TRN_SPD = 90

RB = 0.11  # Half distance between wheels, need to measure in lab
RW = 0.028  # Wheel radius
DISTTODEG = (180 / (math.pi * RW))
ORIENTTODEG = RB / RW

def wait_for_motor(Motor):
    # Wait for motor to spin or slow down
    while math.isclose(motor.get_speed(), 0):
        time.sleep(MOTOR_POLL_DELAY)
    while not math.isclose(motor.get_speed, 0):
        time.sleep(MOTOR_POLL_DELAY)

def init_motor(Motor):
        motor.reset_encoder()
        motor.set_limits(POWER_LMIT, SPEED_LIMIT)
        motor.set_power(0)

def init_motor(Motor):
        motor.reset_encoder()
        motor.set_limits(POWER_LMIT, SPEED_LIMIT)
        motor.set_power(0)

def moveForward(distance, speed):
    LEFT_MOTOR.set_dps(speed)
    RIGHT_MOTOR.set_dps(speed)

    LEFT_MOTOR.set_limits(POWER_LIMIT, speed)
    RIGHT_MOTOR.set_limits(POWER_LIMITS, speed)

    LEFT_MOTOR.set_position_relative(int(distance*DISTTODEG))
    RIGHT_MOTOR.set_position_relative(int(distance*DISTTODEG))

    wait_for_motor(RIGHT_MOTOR)


def moveForwardUntilObstacle():
    while US_SENSOR.get_distance() > 0.1:
        time.sleep(MOTOR_POLL_DELAY)
    
    stopMotors()

def moveBackward(speed):
     LEFT_MOTOR.set_dps(speed)
     RIGHT_MOTOR.set_dps(speed)

     LEFT_MOTOR.set_limits(POWER_LIMIT, speed)
     RIGHT_MOTOR.set_limits(POWER_LIMITS, speed)

     LEFT_MOTOR.set_position_relative(-int(distance*DISTTODEG))
     RIGHT_MOTOR.set_position_relative(-int(distance*DISTTODEG))

     wait_for_motor(RIGHT_MOTOR)
          
          

def rotate(angle):
    LEFT_MOTOR.set_limits(POWER_LIMIT, TRN_SPD)
    RIGHT_MOTOR.set_limits(POWER_LIMIT, TRN_SPD)

    LEFT_MOTOR.set_position_relative(-int(angle * ORIENTTODEG))
    RIGHT_MOTOR.set_position_relative(int(angle * ORIENTTODEG))
    wait_for_motor(RIGHT_MOTOR)

def stopMotors():
    LEFT_MOTOR.set_dps(0)
    RIGHT_MOTOR.set_dps(0)

def turnLeft(angle=90):
    rotate(angle)

def turnRight(angle=90):
    rotate(-angle)



