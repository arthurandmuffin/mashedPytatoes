from utils import statics, maps

#creates a map
navMap = maps.Map(20, 20, 10, 10, 90)

navMap.markCurrentLocationAsVisited(45, [2, 3], 2)
navMap.print_grid()

