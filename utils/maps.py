from . import statics

import math, statistics

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
    def __init__(self, gridWidthCount, gridLengthCount, initX, initY, initOrientation):
        self.gridWidthCount = gridWidthCount
        self.gridLengthCount = gridLengthCount
        self.grid = [[MapCell() for _ in range(gridWidthCount)] for _ in range(gridLengthCount)]
        self.currentLocationX = initX #shouldnt be 0 or gridCount, range must be robotWidthRadius / robotLengthRadius
        self.currentLocationY = initY
        self.currentOrientation = initOrientation

    def print_grid(self):
        for row in self.grid:
            print("".join(str(cell) for cell in row))
            
    def UpdateCurrentLocation(self, grid):
        if grid[0] < 0 or grid[1] < 0 or grid[0] > self.gridWidthCount - 1 or grid[1] > self.gridLengthCount - 1:
            return False
        self.currentLocationX, self.currentLocationY = grid[0], grid[1]
        print("X: " + str(self.currentLocationX) + ", Y: " + str(self.currentLocationY))
        return True

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
                
    def MarkVisitedPath(self, initialLeft, initialRight, currentLeft, currentRight, robotDimensions):
        #Distance travelled
        wheelRotations = (statistics.mean([currentLeft - initialLeft, currentRight - initialRight]) / 360)
        distanceTravelled = (wheelRotations * statics.WheelCircumference * statics.StraightLineOffset) * statics.DistanceTravelledCorrectionFactor
        
        #Starting coordinates
        initialGrid = [self.currentLocationX, self.currentLocationY]
        initialCoords = Map.gridToCoords(initialGrid)
        
        #Current coordinates
        orientation_radians = math.radians(self.currentOrientation)
        currentCoords = [initialCoords[0] - math.sin(orientation_radians) * distanceTravelled, initialCoords[1] + math.cos(orientation_radians) * distanceTravelled]
        
        #Centre point
        centrePointGrids = Map.coordsToGrid([(initialCoords[0] + currentCoords[0]) / 2, (initialCoords[1] + currentCoords[1]) / 2])
        if not self.UpdateCurrentLocation(centrePointGrids):
            print("Grid fucked")
        print([robotDimensions[0], round((math.dist(initialCoords, currentCoords) / 2) / statics.GridCellDimension)])
        self.markCurrentLocationAsVisited(self.currentOrientation, [robotDimensions[0], round((math.dist(initialCoords, currentCoords) / 2) / statics.GridCellDimension)], 0)
        self.UpdateCurrentLocation(initialGrid)
        return [self.currentLocationX, self.currentLocationY]
    
    def DistanceFromWallsToCurrentGrid():
        raise None
    
    def MarkObstacle(self, colourSensorLocation, currentGrid = None, currentCoords = None):
        if currentGrid is None and currentCoords is None: raise ValueError
        
        if currentCoords is None:
            currentCoords = Map.gridToCoords(currentGrid)
            
        if self.currentOrientation == statics.Direction.NORTH:
            obstacleCoords = [currentCoords[0] - colourSensorLocation[1], currentCoords[1] + colourSensorLocation[0]]
        elif self.currentOrientation == statics.Direction.SOUTH:
            obstacleCoords = [currentCoords[0] + colourSensorLocation[1], currentCoords[1] + colourSensorLocation[0]]
        elif self.currentOrientation == statics.Direction.EAST:
            obstacleCoords = [currentCoords[0] - colourSensorLocation[0], currentCoords[1] - colourSensorLocation[1]]
        elif self.currentOrientation == statics.Direction.WEST:
            obstacleCoords = [currentCoords[0] + colourSensorLocation[0], currentCoords[1] + colourSensorLocation[1]]
        obstacleGridCell = self.getMapCell(Map.coordsToGrid(obstacleCoords))
        obstacleGridCell.isObstacle = True
    
    def MarkWater(self, colourSensorLocation, currentGrid = None, currentCoords = None):
        if currentGrid is None and currentCoords is None: raise ValueError

        if currentCoords is None:
            currentCoords = Map.gridToCoords(currentGrid)
        
        if self.currentOrientation == statics.Direction.NORTH:
            waterCoords = [currentCoords[0] - colourSensorLocation[1], currentCoords[1] + colourSensorLocation[0]]
        elif self.currentOrientation == statics.Direction.SOUTH:
            waterCoords = [currentCoords[0] + colourSensorLocation[1], currentCoords[1] + colourSensorLocation[0]]
        elif self.currentOrientation == statics.Direction.EAST:
            waterCoords = [currentCoords[0] - colourSensorLocation[0], currentCoords[1] - colourSensorLocation[1]]
        elif self.currentOrientation == statics.Direction.WEST:
            waterCoords = [currentCoords[0] + colourSensorLocation[0], currentCoords[1] + colourSensorLocation[1]]
        waterGrid = Map.coordsToGrid(waterCoords)
        waterGridCell = self.getMapCell(Map.coordsToGrid(waterCoords))
        waterGridCell.isWater = True
        self.traceWaterCells(waterGrid, self.nearbyWaterCells(waterGrid, statics.WaterMaxTraceDistance))
        
    def nearbyWaterCells(self, grid, distanceThreshold):
        res = []
        for x in range(-distanceThreshold, distanceThreshold + 1):
            for y in range(-distanceThreshold, distanceThreshold + 1):
                cellX, cellY = grid[0] + x, grid[1] + y
                if 0 <= cellX < self.gridWidthCount and 0 <= cellY < self.gridLengthCount and self.grid[cellX][cellY].isWater:
                    res.append([cellX, cellY])
        return res
    
    def traceWaterCells(self, grid, nearbyWaterCells):
        for cell in nearbyWaterCells:
            x1, y1 = grid[0], grid[1]
            x2, y2 = cell[0], cell[1]
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            stepX = 1 if x2 > x1 else -1 if x2 < x1 else 0
            stepY = 1 if y2 > y1 else -1 if y2 < y1 else 0
            
            err = dx - dy
            while (x1, y1) != (x2, y2):
                self.grid[x1][y1].isWater = True
                err2 = err * 2
                if err2 > -dy:
                    err -= dy
                    x1 += stepX
                if err2 < dx:
                    err += dx
                    y1 += stepY
            self.grid[x2][y2].isWater = True
            
    def fillWaterSurroundedCells(self):
        visited = set()
        
        def floodFill(initX, initY):
            queue = [(initX, initY)]
            visited.add((initX, initY))
            
            while queue:
                x, y = queue.pop()
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    newX, newY = x + dx, y + dy
                    if 0 <= newX < self.gridWidthCount and 0 <= newY < self.gridLengthCount and (newX, newY) not in visited:
                        if not self.grid[newX][newY].isWater:
                            queue.append((newX, newY))
                            visited.add((newX, newY))
                            
        for x in range(self.gridWidthCount):
            for y in [0, self.gridLengthCount - 1]:
                if not self.grid[x][y].isWater and (x, y) not in visited:
                    floodFill(x, y)
                    
        for y in range(self.gridLengthCount):
            for x in [0, self.gridWidthCount - 1]:
                if not self.grid[x][y].isWater and (x, y) not in visited:
                    floodFill(x, y)
                    
        for x in range(self.gridWidthCount):
            for y in range(self.gridLengthCount):
                if (x, y) not in visited:
                    self.grid[x][y].isWater = True

    def getMapCell(self, gridCoord):
        return self.grid[gridCoord[0]][gridCoord[1]]
    
    def ValidGrid(self, grid):
        if 0 <= grid[0] < self.gridWidthCount and 0 <= grid[1] < self.gridLengthCount:
            return True
        return False
    
    @staticmethod
    # Takes in [xgrid, ygrid] returns [xcoord, ycoord]
    def gridToCoords(grid):
        return [(x + 0.5) * statics.GridCellDimension for x in grid]
    
    @staticmethod
    # v.v. from gridToCoords
    def coordsToGrid(coords):
        return [math.floor(x / statics.GridCellDimension) for x in coords]