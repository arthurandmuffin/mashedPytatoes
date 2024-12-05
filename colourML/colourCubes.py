# Trains a decision tree, given RGB values, to determine colour of cubes

from sklearn.tree import DecisionTreeClassifier, export_text

filenames = ["greenCube.txt", "purpleCube.txt", "orangeCube.txt", "yellowCube.txt"]
colour = ["GreenCube", "PurpleCube", "OrangeCube", "YellowCube"]

data = []
for i in range(len(filenames)):
    with open(filenames[i], 'r') as file:
        lines = file.readlines()
    for line in lines:
        entry = eval(line.strip())
        entry.append(colour[i])
        data.append(entry)

colourFeatures = [row[:3] for row in data]
colourLabels = [row[4] for row in data]

colourTree = DecisionTreeClassifier(criterion="entropy")
colourTree.fit(colourFeatures, colourLabels)

treeRules = export_text(colourTree, feature_names=["R", "G", "B"])

print(treeRules)