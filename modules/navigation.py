from utils import maps, statics, movement

import heapq
from time import sleep

#   TODO:
#   1. Incorporate self locate?
#   2. Flood edge lakes + unvisitable areas?
#   3. Bridge?? Only visit on way back (extra thing to handle), recognize bridge (how?)

def Navigatefuckingeverything(leftMotor, rightMotor, armMotor, clawMotor, leftCS, rightCS, frontUS, sideUS, navMap):
    shitCount = 0
    pathQueue = []
    movement.moveForwardUntilObstacle() #need to change this to handle distance too?, pass shitcount
    pathQueue = visitNearestUnknown(navMap)
    while shitCount <= 6:
        if len(pathQueue) == 0:
            pathQueue = visitNearestUnknown(navMap)
            continue
        nextPath = pathQueue.pop()
        movement.moveForwardUntilObstacle(leftMotor, rightMotor, frontUS, sideUS, leftCS, rightCS, getDistance(nextPath), navMap)
        reorient(nextPath, pathQueue[0])
    
    #go back? set home coords statics
    pathHome = pathPlanToPaths(pathToCell(navMap, (0, 50)))
    while len(pathHome) != 0:
        movement.moveForwardUntilObstacle(pathHome.pop())

#rewrite this shit, straight ass
def visitNearestUnknown(navMap):
    x, y = navMap.currentLocationX, navMap.currentLocationY
    random = 20
    newTarget = largestClump(navMap, nearbyUnvisitedCells(navMap, random))
    while len(newTarget) == 0:
        random += 10
        newTarget = largestClump(navMap, nearbyUnvisitedCells(navMap, random))
    pathPlanToPaths(pathToCell(navMap, newTarget[0]))
    
def largestClump(navMap, unvisitedCells):
    visited = set() #processed, not actually visited
    largestClump = [] #for now just take 1st element as target, possible optimisation to avoid turns?
    cutoff = statics.MaximumUnvisitedClumpSize
    
    for cell in unvisitedCells:
        if cell not in visited:
            clump = []
            queue = [cell]
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                clump.append(current)
                
                for x, y in neighbours(current):
                    if not navMap.grid[x][y].visited and [x, y] not in visited:
                        queue.append((x, y))
                        
                if len(clump) > cutoff:
                    break
            
            if len(clump) > len(largestClump):
                largestClump = clump
    
    return largestClump
                
def neighbours(grid):
    x, y = grid
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    
def nearbyUnvisitedCells(navMap, distanceThreshold):
    res = []
    for x in range(-distanceThreshold, distanceThreshold + 1):
        for y in range(-distanceThreshold, distanceThreshold + 1):
            cellX, cellY = navMap.grid[0] + x, navMap.grid[1] + y
            if 0 <= cellX < navMap.gridWidthCount and 0 <= cellY < navMap.gridLengthCount and not navMap.grid[cellX][cellY].visited:
                res.append((cellX, cellY))
    return res

def pathToCell(navMap, target):
    initX, initY = navMap.currentLocationX, navMap.currentLocationY
    initAxis = orientationToAxis(navMap.currentOrientation)
    targetX, targetY = target[0], target[1]
    
    orientationsToExplore = [("X-axis", 1, 0), ("X-axis", -1, 0), ("Y-axis", 0, 1), ("Y-axis", 0, -1)]
    
    def heuristic(x, y):
        return abs(targetX - x) + abs(targetY - y)
    
    def straightMoveValid(x, y):
        #Coord in question
        if not navMap.ValidGrid([x, y]):
            return False
        if navMap.grid[x][y].isWater or navMap.grid[x][y].isObstacle:
            return False
        
        #Surroundings
        for dx in range(-statics.RobotGridWidth, statics.RobotGridWidth + 1):
            for dy in range(-statics.RobotGridWidth, statics.RobotGridWidth + 1):
                x1, y1 = x + dx, y + dy
                if not navMap.ValidGrid([x1, y1]):
                    return False
                if navMap.grid[x1][y1].isWater or navMap.grid[x1][y1].isObstacle:
                    return False
        return True
    
    def rotationValid(x, y):
        #Coord in question
        if not navMap.ValidGrid([x, y]):
            return False
        if navMap.grid[x][y].isWater or navMap.grid[x][y].isObstacle:
            return False
        
        #Surroundings
        for dx in range(-statics.RobotGridLength, statics.RobotGridLength + 1):
            for dy in range(-statics.RobotGridLength, statics.RobotGridLength + 1):
                x1, y1 = x + dx, y + dy
                if not navMap.ValidGrid([x1, y1]):
                    return False
                if navMap.grid[x1][y1].isWater or navMap.grid[x1][y1].isObstacle:
                    return False
        return True
    
    openSet = []
    
    # Priority queue: (f(n), g(n), x, y, orientation, path)
    heapq.heappush(openSet, (heuristic(initX, initY), 0, initX, initY, initAxis, [(initX, initY)]))
    visited = set()
    
    while openSet:
        _, g, x, y, axis, path = heapq.heappop(openSet)

        if [x, y] == [targetX, targetY]:
            return path + [(x, y)]
        
        if (x, y, axis) in visited:
            continue
        visited.add((x, y, axis))
        
        for newAxis, dx, dy in orientationsToExplore:
            newX, newY = x + dx, y + dy
            
            if axis == newAxis:
                if straightMoveValid(newX, newY) and (newX, newY, newAxis) not in visited:
                    heapq.heappush(openSet, (g + 1 + heuristic(newX, newY), g + 1, newX, newY, newAxis, path))
            else:
                if rotationValid(x, y) and rotationValid(newX, newY) and (newX, newY, newAxis) and (newX, newY, newAxis) not in visited:
                    heapq.heappush(openSet, (g + 2 + heuristic(newX, newY), g + 2, newX, newY, newAxis, path + [(x, y)]))
    
def orientationToAxis(orientation):
    if orientation == statics.Direction.NORTH.value or orientation == statics.Direction.SOUTH.value:
        return "X-axis"
    return "Y-axis"

def pathPlanToPaths(pathPlan):
    return [[pathPlan[i], pathPlan[i+1]] for i in range(len(pathPlan) - 1)]

def reorient(currentPath, nextPath, leftMotor, rightMotor):
    x0, y0 = currentPath[0]
    x1, y1 = currentPath[1]
    x2, y2 = nextPath[1]
    
    v1X = x1 - x0
    v1Y = y1 - y0
    v2X = x2 - x1
    v2Y = y2 - y1
    
    crossProduct = (v1X * v2Y) - (v1Y * v2X)
    if crossProduct > 0:
        #rotate left
        movement.rotateLeft90(leftMotor, rightMotor)
        sleep(1)
    elif crossProduct < 0:
        #rotate right
        movement.rotateRight90(leftMotor, rightMotor)
        sleep(1)
    else:
        print("retard")
        
def getDistance(path):
    coord1 = path[0]
    coord2 = path[1]
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])