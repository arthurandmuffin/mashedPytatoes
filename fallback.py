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

navMap = maps.Map(48, 48, 5, 5, 90)
wait_ready_sensors(True)
coord = (11, 14)
orientation = statics.Direction.EAST
#crane.findStandardZero(CLAW)
ARM.set_limits(50, 100)
CLAW.set_limits(50, 100)
#crane.idle(ARM, CLAW)
#movement.stopMotors(leftMotor, rightMotor)
distanceTravelled = movement.moveForwardFallback(leftMotor, rightMotor, ARM, CLAW, frontUS, sideUS, leftCS, rightCS, None)
print(distanceTravelled)
#reset_brick()