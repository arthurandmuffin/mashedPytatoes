#DEMO CODE

from utils import movement, colour, statics, maps
from time import sleep

from brickUtils.brick import BP, EV3UltrasonicSensor, Motor, wait_ready_sensors, reset_brick, EV3ColorSensor
from modules import selfLocate, crane, navigation

leftMotor = Motor("C")
rightMotor = Motor("B")
doorMotor = Motor("D")
US_SENSOR = EV3UltrasonicSensor(2)
COLOUR_RIGHT = EV3ColorSensor(1)
COLOUR_LEFT = EV3ColorSensor(3)

wait_ready_sensors(True)
#reset_brick()
#movement.stopMotors(leftMotor, rightMotor)
movement.init_motor(leftMotor)
movement.init_motor(rightMotor)
movement.init_motor(doorMotor)
sleep(1)
doorMotor.set_position(0)
distanceTravelled = movement.moveForwardFallback(leftMotor, rightMotor, doorMotor, US_SENSOR, COLOUR_LEFT, COLOUR_RIGHT, None)
movement.moveBackAfterObstacle(leftMotor, rightMotor, distanceTravelled + 20)