import time
import math
from utils import brick
from utils import BP, EV3UltrasonicSensor, Motor, TouchSensor, wait_ready_sensors
from utils.statics import Direction, WallMeasurment

# set up
SAMPLING_INTERVAL = 0.2
DEFAULT_WALL_DIST = 0.15
US_OUTLIER = 255
MOTOR_POLL_DELAY = 0.05
US_SENSOR = EV3UltrasonicSensor(2) 
LEFT_MOTOR = Motor("A")
RIGHT_MOTOR = Motor("D")

BOX_WIDTH = 1.22
BOX_LENGTH = 1.22

POWER_LIMIT = 80
SPEED_LIMIT = 270
TRN_SPD = 90

RB = 0.09  # Half distance between wheels
RW = 0.028  # Wheel radius
DISTTODEG = (180 / (3.1416 * RW))
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

def rotate_90():
     angle = 90
     try:
        LEFT_MOTOR.set_limits(POWER_LIMIT, TRN_SPD)
        RIGHT_MOTOR.set_limits(POWER_LIMIT, TRN_SPD)

        LEFT_MOTOR.set_position_relative(int(angle * ORIENTTODEG))
        RIGHT_MOTOR.set_position_relative(-int(angle * ORIENTTODEG))
        
        wait_for_motor(LEFT_MOTOR)
        wait_for_motor(RIGHT_MOTOR)
     except IOError as error:
        print("Motor error:", error)


def take_measurements():
     distances = []
     directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
     for direction in directions:
        dist = US_SENSOR.get_cm() / 100.0
        distances.append(WallMeasurement(direction, distance))
        rotate_90()
        time.sleep(SAMPLING_INTERVAL)
     return distances

def calculate_position(distances):
    


        
