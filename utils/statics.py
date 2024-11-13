from enum import Enum, auto
import math

class WallMeasurement:
    def __init__(self, orientation, distance):
        self.orientation = orientation
        self.distance = distance

class Direction(Enum):
    NORTH = 90
    SOUTH = 270
    EAST = 0
    WEST = 180

MotorPollDelay = 0.05
USSensorPort = 2
LeftMotorPort = "A"
RightMotorPort = "D"
MotorPowerLimit = 80
MotorSpeedLimit = 270
MotorTurnSpeed = 90
WheelRadius = 0.028 #check
HalfWheelBase = 0.11 #check
DistToDeg = (180 / (math.pi * WheelRadius))
OrientToDeg = HalfWheelBase/WheelRadius
    
MapWidth = 0 #check
MapLength = 0 #check
MapWidthInGrids = 49
MapLengthInGrids = 49
GridCellDimension = 2.54 #width/length of 1 map cell
LeftColourSensorLocation = []
RightColourSEnsorLocation = []

RightAngleOrientations = [0, 90, 180, 270]

USSensorMedianFilterWindowSize = 5
USSensorErrorValue = 255.0
WallDistanceDataPointCount = 20
USSensorOffsetFromRobotCentre = 2 #distance from us sensor to centre of robot