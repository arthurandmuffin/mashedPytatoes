from . import statics

import math

class MapCell:
    def __init__(self):
        self.visited = False
        self.isObstacle = False
        self.isWater = False
        self.isStart = False
        self.isTrashCan = False

    def __str__(self):
        if self.visited == True:
            return "V"
        elif self.isWater == True:
            return "O"
        else:
            return "_"
        #return f"Visited: {self.visited}, Obstacle: {self.isObstacle}, Water: {self.isWater}, Start: {self.isStart}, TrashCan: {self.isTrashCan}"

class Map:
    def __init__(self, gridWidthCount, gridLengthCount, initX, initY):
        self.gridWidthCount = gridWidthCount
        self.gridLengthCount = gridLengthCount
        self.grid = [[MapCell() for _ in range(gridWidthCount)] for _ in range(gridLengthCount)]
        self.currentLocationX = initX #shouldnt be 0 or gridCount, range must be robotWidthRadius / robotLengthRadius
        self.currentLocationY = initY

    def print_grid(self):
        for row in self.grid:
            print("".join(str(cell) for cell in row))

    def markCurrentLocationAsVisited(self, orientationDegrees, robotDimensions, observedGridCount):
        robotWidthRadius, robotLengthRadius = robotDimensions
        currentLocation = [self.currentLocationX, self.currentLocationY]
        orientation_radians = math.radians(orientationDegrees)

        forward_distance = robotLengthRadius + observedGridCount

        markedCoords = []
        rowBoundaries = {}

        for dx in range(-robotWidthRadius, robotWidthRadius + 1):
            for dy in range(-robotLengthRadius, forward_distance + 1):
                rotated_x = round(currentLocation[0] + (dx * math.cos(orientation_radians) - dy * math.sin(orientation_radians)))
                rotated_y = round(currentLocation[1] + (dx * math.sin(orientation_radians) + dy * math.cos(orientation_radians)))
                
                if 0 <= rotated_x < self.gridLengthCount and 0 <= rotated_y < self.gridWidthCount:
                    self.grid[rotated_x][rotated_y].visited = True
                    markedCoords.append([rotated_x, rotated_y])

        for coord in markedCoords:
            x = coord[0]
            if x not in rowBoundaries:
                rowBoundaries[x] = []
            rowBoundaries[x].append(coord[1])
        
        for rowX, yValues in rowBoundaries.items():
            for y in range(min(yValues), max(yValues) + 1):
                self.grid[rowX][y].visited = True

    def UpdateCurrentLocation():
        raise None
    
    def DistanceFromWallsToCurrentGrid():
        raise None
    
    def AddObstacle():
        raise None
    
    def MarkWater(self, colourSensorLocation, currentGrid = None, currentCoords = None):
        if currentGrid is None and currentCoords is None: raise ValueError

        if currentCoords is None:
            currentCoords = Map.gridToCoords(currentGrid)
        
        waterCoords = [currentCoord + sensorLocation for currentCoord, sensorLocation in zip(currentCoords, colourSensorLocation)]
        waterGridCell = self.getMapCell(Map.coordsToGrid(waterCoords))
        waterGridCell.isWater = True

        self.FloodFillWater(waterCoords)

    def getMapCell(self, gridCoord):
        return self.grid[gridCoord[0]][gridCoord[1]]
    
    @staticmethod
    def gridToCoords(grid):
        return [(x + 0.5) * statics.GridCellDimension for x in grid]
    
    @staticmethod
    def coordsToGrid(coords):
        return [math.floor(x / statics.GridCellDimension) for x in coords]

    def FloodFillWater(self):
        for x in range(self.gridWidthCount):
            for y in range(self.gridLengthCount):
                if not self.grid[x,y].isWater:
                    if self.isSurroundingWater(x, y):
                        self.grid[x][y].isWater = True
    
    def isSurroundingWater(self, x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        count = 0

        for dx, dy in directions:
            ex, ey = x + dx, y + dy
            if 0 <= ex < self.gridLengthCount and 0 <= ey < self.gridWidthCount:
                if self.grid[ex][ey].isWater:
                    count += 1
                if count >= 3:
                    return True
                
        return False
