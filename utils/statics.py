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

class ColourTargetType(Enum):
    GROUND = "Ground"
    CUBE = "Cube"

class GroundColours(Enum):
    WATER = "Water"
    GRIDLINE = "Gridline"
    GRASS = "Grass"

class CubeColours(Enum):
    PURPLE = "PurpleCube"
    ORANGE = "OrangeCube"
    GREEN = "GreenCube"
    YELLOW = "YellowCube"
    
    def isPoop(self):
        # return self in {CubeColours.PURPLE, CubeColours.ORANGE} # yo whatttt
        return self in {CubeColours.YELLOW, CubeColours.ORANGE}
FrontUSSensorPort = 2
SideUSSensorPort = 0
LeftColourPort = 0
RightColourPort = 0
LeftMotorPort = "A"
RightMotorPort = "D"
ArmMotorPort = ""
ClawMotorPort = ""

MotorPollDelay = 0.05
MotorPowerLimit = 80
MotorSpeedLimit = 270
MotorTurnSpeed = 90
WheelRadius = 2.2 #check
WheelCircumference = 2 * math.pi * WheelRadius
WheelBase = 7.7 #check
DistToDeg = (180 / (math.pi * WheelRadius))
StraightLineOffset = 1
    
MapWidth = 50 #check
MapLength = 50 #check
MapWidthInGrids = 49
MapLengthInGrids = 49
GridCellDimension = 2.54 #width/length of 1 map cell
LeftColourSensorLocation = [2, 3]
RightColourSensorLocation = []
WaterMaxTraceDistance = 3

RightAngleOrientations = [0, 90, 180, 270]

USSensorMedianFilterWindowSize = 5
USSensorErrorValue = 255.0
WallDistanceDataPointCount = 20
USSensorOffsetFromRobotCentre = 2 # distance from us sensor to centre of robot

CruisingPower = -50
CruisingSpeed = -130
DeviationLimit = 1
TrackingThreshold = 20
PickupThreshold = 6
SpeedCorrectionFactor = 1.2
CorrectionTimer = 1
DistanceTravelledCorrectionFactor = 1

# CRANE SUBSYSTEM
armIdle = -70
clawIdle = 60

armPickup = -95
armDrop = 95
armUnload = -220

clawOpen = 50
clawClose = 120
clawUnload = -180