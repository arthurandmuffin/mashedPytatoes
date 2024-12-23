# Classify colour sensor reading as
# Floor: 
#    - Water
#    - Grass
#    - Gridline
# Cube:
#    - Green Cube
#    - Purple Cube
#    - Yellow Cube
#    - Orange Cube

from utils import statics

def getObject(rgbValues):
    if rgbValues == None:
        return None
    targetType = classifyTarget(rgbValues)
    if targetType == statics.ColourTargetType.GROUND:
        return classifyFloor(rgbValues)
    else:
        return classifyCube(rgbValues)

def classifyTarget(rgbValues):
    if rgbValues == None:
        return None
    avg = sum(rgbValues[:3]) / 3
    if avg <= 36:
        return statics.ColourTargetType.GROUND
    else:
        return statics.ColourTargetType.CUBE

def classifyFloor(rgbValues):
    R = rgbValues[0]
    G = rgbValues[1]
    B = rgbValues[2]
    if G <= 13.50:
        if R <= 7.50:
            return statics.GroundColours.WATER
        else:
            if G <= 12.50:
                return statics.GroundColours.GRIDLINE
            else:
                if R <= 13.00:
                    return statics.GroundColours.GRASS
                else:
                    return statics.GroundColours.GRIDLINE
    else:
        if R <= 14.50:
            return statics.GroundColours.GRASS
        else:
            if B <= 6.00:
                return statics.GroundColours.GRIDLINE
            else:
                return statics.GroundColours.GRASS

def classifyCube(rgbValues):
    R = rgbValues[0]
    G = rgbValues[1]
    B = rgbValues[2]
    if R <= 100:
        if R <= 39.00:
            return statics.CubeColours.GREEN
        else:
            return statics.CubeColours.PURPLE
    else:
        if B <= 33.00:
            return statics.CubeColours.YELLOW
        else:
            return statics.CubeColours.ORANGE