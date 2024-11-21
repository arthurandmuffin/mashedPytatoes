from sklearn.tree import DecisionTreeClassifier, export_text
import math

with open('allFloor.txt', 'r') as floor:
    lines = floor.readlines()

floorData = []
for line in lines:
    data = eval(line.strip())
    floorData.append([sum(data[:3]) / 3])

#floorData = [eval(line.strip()) for line in lines]
for data in floorData:
    data.append('floor')

with open('closeUp.txt', 'r') as close:
    lines = close.readlines()

closeUpData = []
for line in lines:
    data = eval(line.strip())
    closeUpData.append([sum(data[:3]) / 3])

#closeUpData = [eval(line.strip()) for line in lines]
for data in closeUpData:
    data.append('closeUp')

distanceData = floorData + closeUpData

distanceFeature = [[row[0]] for row in distanceData]
distanceLabel = [[row[1]] for row in distanceData]

distanceTree = DecisionTreeClassifier()
distanceTree.fit(distanceFeature, distanceLabel)

treeRules = export_text(distanceTree, feature_names=["avg"])
print(treeRules)