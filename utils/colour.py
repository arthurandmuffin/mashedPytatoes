def getObject(rgbValues):
    if rgbValues == None:
        return None
    if classifyTarget(rgbValues) == "Ground":
        return classifyFloor(rgbValues)
    else:
        return classifyCube(rgbValues)

def classifyTarget(rgbValues):
    if rgbValues == None:
        return None
    avg = sum(rgbValues[:3]) / 3
    if avg <= 30.17:
        return "Ground"
    else:
        return "Cube"

def classifyFloor(rgbValues):
    if rgbValues == None:
        return None
    R = rgbValues[0]
    G = rgbValues[1]
    B = rgbValues[2]
    if G <= 13.50:
        if R <= 7.50:
            return "Water"
        else:
            if G <= 12.50:
                return "Gridline"
            else:
                if R <= 13.00:
                    return "Grass"
                else:
                    return "Gridline"
    else:
        if R <= 14.50:
            return "Grass"
        else:
            if B <= 6.00:
                return "Gridline"
            else:
                return "Grass"

def classifyCube(rgbValues):
    if rgbValues == None:
        return None
    R = rgbValues[0]
    G = rgbValues[1]
    B = rgbValues[2]
    if R <= 137.50:
        if R <= 39.00:
            return "GreenCube"
        else:
            return "PurpleCube"
    else:
        if B <= 33.00:
            return "YellowCube"
        else:
            return "OrangeCube"

def isPoop(rgbValues):
    if classifyCube(rgbValues) == "GreenCube" or classifyCube(rgbValues) == "PurpleCube":
        return "isObstacle"
    elif classifyCube(rgbValues) == "YellowCube" or classifyCube(rgbValues) == "OrangeCube":
        return "isPoop"
    else:
        return "isNotEvenCube"
    