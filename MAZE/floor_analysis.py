import ast

def readFile(path):
    with open(path, "rt") as f:
        return f.read()
        
def getFloorPlan(info):
    levelString = ""
    toggleRead = False
    count = 0
    for elem in info:
        if elem=="\n" and count<2:
            toggleRead = not toggleRead
            count+=1
        if toggleRead:
            levelString +=elem
    return ast.literal_eval(levelString)

##
floorPlan = getFloorPlan(readFile("Level_Info.txt"))

def valid(floor,j,i):
    try:
        floor[j][i]
        return True
    except:
        return False
        
def makeNodes(floorPlan):
    nodeIndexes = []
    for j in range(len(floorPlan)):
        for i in range(len(floorPlan)):
            if check(floorPlan,j,i):
                nodeIndexes.append((j,i))
    return nodeIndexes


def check(floor,j,i):
    if valid(floor,j-1,i-1) and floor[j-1][i-1]!=0:
        if floor[j-1][i]==0 and floor[j][i-1]==0:
            return True
    if valid(floor,j+1,i-1) and floor[j+1][i-1]!=0:
        if floor[j][i-1]==0 and floor[j+1][i]==0:
            return True
    if valid(floor,j+1,i+1) and floor[j+1][i+1]!=0:
        if floor[j][i+1]==0 and floor[j+1][i]==0:
            return True
    if valid(floor,j-1,i+1) and floor[j-1][i+1]!=0:
        if floor[j][i+1]==0 and floor[j-1][i]==0:
            return True
    return False
    