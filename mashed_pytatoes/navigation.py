from utils import time
import robot

position = [0, 0]
direction = "N"

def move_forward():
    
    
    if direction == "N":
        position[1] += 1
    elif direction == "S":
        position[1] -=1
    elif direction == "E":
        position[0] += 1
    elif direction == "W":
        position[0] -= 1
        
def handle_obstacle():
    robot.stop()
    robot.move_backwards(safe_distance)
    robot.turn_right(45)
    robot.move_forward(adjusted_path)
    

