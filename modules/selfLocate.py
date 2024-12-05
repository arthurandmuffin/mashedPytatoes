# Rotate and take distances from walls to triangulate current position on map
# Used to self correct during nav to avoid noise / error compounding

from utils import calculations, movement, maps, statics

from statistics import mean

def SelfLocate(currentOrientation, motorL, motorR, usSensor):
    distancesFromWalls = sorted(getDistanceFromWalls(currentOrientation, motorL, motorR, usSensor), key=lambda x: x[1])[:2]
    orientationMap = {
        statics.Direction.EAST: lambda distance: (statics.MapWidthInGrids - (distance // statics.GridCellDimension) - 1, statics.MapWidth - distance),
        statics.Direction.NORTH: lambda distance: (distance // statics.GridCellDimension, distance),
        statics.Direction.WEST: lambda distance: (distance // statics.GridCellDimension, distance),
        statics.Direction.SOUTH: lambda distance: (statics.MapLengthInGrids - (distance // statics.GridCellDimension) - 1, statics.MapLength - distance),
    }

    xGrid, yGrid = None, None
    xCoord, yCoord = None, None

    for orientation, distance in distancesFromWalls:
        if orientation in [statics.Direction.EAST, statics.Direction.WEST]:
            xGrid, xCoord = orientationMap[orientation](distance)
        elif orientation in [statics.Direction.NORTH, statics.Direction.SOUTH]:
            yGrid, yCoord = orientationMap[orientation](distance)
    
    if xGrid is None or yGrid is None:
        raise ValueError()

    return (xGrid, yGrid, xCoord, yCoord)

def getDistanceFromWalls(orientation, motorL, motorR, usSensor):
    correctionAngle = getOrientationCorrection(orientation)
    distancesFromWalls = []

    orientation = movement.rotate(correctionAngle, motorR, motorL, orientation)
    for _ in range(4):
        distancesFromWalls.append([orientation, getUsSensorData(usSensor) + statics.USSensorOffsetFromRobotCentre])
        orientation = movement.rotate(90, motorR, motorL, orientation)
    orientation = movement.rotate(-correctionAngle, motorR, motorL, orientation)

    return distancesFromWalls

def getUsSensorData(usSensor):
    data = []
    while len(data) <= statics.WallDistanceDataPointCount:
        distance = usSensor.get_value()
        if distance != statics.USSensorErrorValue:
            data.append(usSensor.get_value())
    
    filteredData = calculations.medianFilter(data, statics.USSensorMedianFilterWindowSize)
    return mean(filteredData)

def getOrientationCorrection(orientationDegree):
    if orientationDegree in statics.RightAngleOrientations:
        return 0
    return 90 - orientationDegree