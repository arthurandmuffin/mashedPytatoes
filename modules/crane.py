from utils import statics
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

def pickup(armMotor, clawMotor):
    idle(armMotor, clawMotor)
    sleep(1)
    clawMotor.set_position(statics.clawOpen) # 1. open claw
    sleep(2)
    armMotor.set_position(statics.armPickup) # 2. lower arm
    sleep(2)
    clawMotor.set_position(statics.clawClose) # 3. close claw
    sleep(1)
    armMotor.set_position(statics.armDrop) # 4. bring cube up over the storage unit
    sleep(3)
    clawMotor.set_position(statics.clawOpen) # 5. drop cube into storage unit
    sleep(3)
    idle(armMotor, clawMotor)
    
def unload(armMotor, clawMotor):
    idle(armMotor, clawMotor)
    armMotor.set_position(statics.armUnload)
    sleep(4)
    idle(armMotor, clawMotor)