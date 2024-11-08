from enum import Enum, auto

class WallMeasurement:
    def __init__(self, orientation, distance):
        self.orientation = orientation
        self.distance = distance

class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()

GridDimension = 49