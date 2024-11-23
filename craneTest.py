from utils import movement, colour
from time import sleep

from brickUtils.brick import BP, EV3UltrasonicSensor, Motor, wait_ready_sensors, reset_brick, EV3ColorSensor
from modules import selfLocate, crane

"""
CHEAT SHEET section:

**** power
motor.set_power(0) --> stops motor
motor.set_power(-50) --> backwards 50 %

**** speed
motor.set_dps(-720) --> backwards 720 deg/sec

**** position
motor.reset_encoder() --> designates to encoder that the current physical position is 0 degrees
motor.set_position(720) --> rotate to 720 degrees away from the 0 position
motor.set_position (700) --> move backwards 20 degrees
motor.get_position() --> returns current position

motor.set_limits(power=50, dps=90) --> limit power and speed
motor.set_position_relative(-180) --> rotate motor to position relative to current position

"""
leftMotor = Motor("B")
rightMotor = Motor("C")
CLAW = Motor("D")
ARM = Motor("A")

frontUS = EV3UltrasonicSensor(1)
sideUS = EV3UltrasonicSensor(4)

leftCS= EV3ColorSensor(2)
rightCS = EV3ColorSensor(3)

ARM.set_limits(50, 100)
CLAW.set_limits(50, 100)

# ----- PROCEDURE TO RESET REFERENCE POSITION -----
## start by verifying 0 degree
# crane.findStandardZero(CLAW) # When claw opens up completely and forms a horizontal line.
# crane.findStandardZero(ARM) # When small motor perpendicular to the ground and claws are parallel to the ground.

# ----- PICKUP-UNLOAD TEST ------------------------
# crane.pickup(ARM, CLAW)
# crane.unload(ARM,CLAW)

# -------------------------------------------------
# while True:
#     movement.moveForwardUntilObstacle(leftMotor, rightMotor, frontUS, sideUS, leftCS, rightCS)
# movement.verifyCube(leftMotor, rightMotor, frontUS)
# movement.stopMotors(leftMotor, rightMotor)
# reset_brick()
while True:
    print(leftCS.get_value())
    sleep(1)