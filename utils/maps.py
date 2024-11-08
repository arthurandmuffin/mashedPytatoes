from statics import Direction

class MapCell:
    def __init__(self):
        self.visited = False
        self.isObstacle = False
        self.isWater = False
        self.isStart = False
        self.isTrashCan = False

class Map:
    def __init__(self, gridCount, initX, initY):
        self.gridCount = gridCount
        self.grid = [[MapCell() for _ in range(gridCount)] for _ in range(gridCount)]
        self.currentLocationX = initX #shouldnt be 0 or gridCount, range must be robotWidthRadius / robotLengthRadius
        self.currentLocationY = initY
    
    def markCurrentAsVisited(self, orientation, robotDimensions, observedGridCount):
        robotWidthRadius, robotLengthRadius = robotDimensions
        currentLocation = [self.currentLocationX, self.currentLocationY]
        orientation_map =  {
            Direction.NORTH : {"lowerX": currentLocation[0] - robotWidthRadius, "upperX": currentLocation[0] + robotWidthRadius, 
                               "lowerY": currentLocation[1] - robotLengthRadius, "upperY": currentLocation[1] + robotLengthRadius + observedGridCount},
            Direction.SOUTH : {"lowerX": currentLocation[0] - robotWidthRadius, "upperX": currentLocation[0] + robotWidthRadius, 
                               "lowerY": currentLocation[1] - robotLengthRadius - observedGridCount, "upperY": currentLocation[1] + robotLengthRadius},
            Direction.EAST : {"lowerX": currentLocation[0] - robotLengthRadius, "upperX": currentLocation[0] + robotLengthRadius + observedGridCount, 
                              "lowerY": currentLocation[1] - robotWidthRadius, "upperY": currentLocation[1] + robotWidthRadius},
            Direction.WEST : {"lowerX": currentLocation[0] - robotLengthRadius - observedGridCount, "upperX": currentLocation[0] + robotLengthRadius, 
                              "lowerY": currentLocation[1] - robotWidthRadius, "upperY": currentLocation[1] + robotWidthRadius},
        }

        boundaries = orientation_map.get(orientation)

        for rowX in range(max(boundaries["lowerX"], 0), min(boundaries["upperX"], self.gridCount)):
            gridRow = self.grid[rowX]
            for cellY in range(max(boundaries["lowerY"], 0), min(boundaries["upperY"], self.gridCount)):
                gridRow[cellY].visited = True

        
    def UpdateCurrentLocation():
        raise None
    
    def DistanceFromWallsToCurrentGrid():
        raise None
    
    def AddObstacle():
        raise None
    
    def MarkWater():
        raise None

    def FloodFillWater():
        raise None
    
