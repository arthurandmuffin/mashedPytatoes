from utils import movement, colour, statics, maps
from time import sleep

from brickUtils.brick import BP, EV3UltrasonicSensor, Motor, wait_ready_sensors, reset_brick, EV3ColorSensor
from modules import selfLocate, crane, navigation

leftMotor = Motor("B")
rightMotor = Motor("C")

clawMotor = Motor("D")
armMotor = Motor("A")

frontUS = EV3UltrasonicSensor(1)
sideUS = EV3UltrasonicSensor(4)

leftCS= EV3ColorSensor(2)
rightCS = EV3ColorSensor(3)

clawMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
armMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
leftMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)
rightMotor.set_limits(statics.MotorPowerLimit, statics.MotorSpeedLimit)

# TODO: Crane Init
#crane.findStandardZero(armMotor)
#crane.findStandardZero(clawMotor)
#crane.idle(armMotor, clawMotor)

# RESET
#movement.stopMotors(leftMotor, rightMotor)

distanceTravelled = movement.moveForwardFallback(leftMotor, rightMotor, armMotor, clawMotor, frontUS, sideUS, leftCS, rightCS, None)
print("Travelled forward: " + str(distanceTravelled))
movement.fuckedupmoveback(leftMotor, rightMotor, distanceTravelled)
print("Done moving back")
movement.rotateLeft90(leftMotor, rightMotor)
distanceTravelled = movement.moveForwardFallback(leftMotor, rightMotor, armMotor, clawMotor, frontUS, sideUS, leftCS, rightCS, None)
print("Travelled forward: " + str(distanceTravelled))
movement.fuckedupmoveback(leftMotor, rightMotor, distanceTravelled)
print("Done moving back")
movement.rotateRight90(leftMotor, rightMotor)
movement.rotateRight90(leftMotor, rightMotor)
crane.unload(armMotor, clawMotor)