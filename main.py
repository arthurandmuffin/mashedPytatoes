#File to run for full map navigation

from utils import movement, colour, statics, maps
from time import sleep

from brickUtils.brick import BP, EV3UltrasonicSensor, Motor, wait_ready_sensors, reset_brick, EV3ColorSensor
from modules import selfLocate, crane, navigation

leftMotor = Motor("B")
rightMotor = Motor("C")

CLAW = Motor("D")
ARM = Motor("A")

frontUS = EV3UltrasonicSensor(1)
sideUS = EV3UltrasonicSensor(4)

leftCS= EV3ColorSensor(2)
rightCS = EV3ColorSensor(3)

navMap = maps.Map(48, 48, 25, 25, 90)

crane.idle(ARM, CLAW)

navigation.NavigateMap(leftMotor, rightMotor, ARM, CLAW, leftCS, rightCS, frontUS, sideUS, navMap)

movement.stopMotors(leftMotor, rightMotor)