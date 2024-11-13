from enum import Enum, auto

class WallMeasurement:
    def __init__(self, orientation, distance):
        self.orientation = orientation
        self.distance = distance

class Direction(Enum):
    NORTH = 90
    SOUTH = 270
    EAST = 0
    WEST = 180

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

