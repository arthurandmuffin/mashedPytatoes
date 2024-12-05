# Crane to pick up and unload cubes into the storage system

from utils import statics, movement
from time import sleep

# Run at the beginning of every lab sessions
def findStandardZero(motor):
    angle = input("Enter angle for reference position of motor: ")
    motor.set_position(angle)
    print(motor.get_position())
    
    is_correct = input("Is the motor at reference position 0 ? [y/n]: ")
    if (is_correct == "y"):
        motor.set_position(angle)
        motor.reset_encoder()
        motor.set_position(0)
        print(motor.get_position())
        return

    else:
        findStandardZero(motor)
    

def idle(armMotor, clawMotor):
    armMotor.set_position(statics.armIdle)
    clawMotor.set_position(statics.clawIdle)

def pickup(leftMotor, rightMotor, doorMotor):
#     idle(armMotor, clawMotor)
#     sleep(1)
#     clawMotor.set_position(statics.clawOpen) # 1. open claw
    sleep(1)
    movement.moveBackwards(leftMotor, rightMotor)
    sleep(2)
    doorMotor.set_position(-100)
    sleep(2)
    movement.init_motor(leftMotor)
    movement.init_motor(rightMotor)
    sleep(0.5)
    leftMotor.set_position_relative(540)
    rightMotor.set_position_relative(540)
    sleep(2)
    doorMotor.set_position(0)
#     sleep(1)
#     armMotor.set_position(statics.armDrop) # 4. bring cube up over the storage unit
#     sleep(2)
#     clawMotor.set_position(statics.clawOpen) # 5. drop cube into storage unit
#     sleep(1)
#     idle(armMotor, clawMotor)
    
def unload(armMotor, clawMotor):
    armMotor.set_position(statics.armPickup)
    sleep(1)
    clawMotor.set_position(statics.clawOpen)
    # idle(armMotor, clawMotor)
    # armMotor.set_position(statics.armUnload)
    # sleep(4)
    # idle(armMotor, clawMotor)