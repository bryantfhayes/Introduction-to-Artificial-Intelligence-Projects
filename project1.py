import sys, Queue

# GLOBAL VARIABLES #
initialStateFile = None
goalStateFile    = None
mode             = None
outputFile       = None
possibleActions  = [[1,0],[2,0],[0,1],[1,1],[0,2]]

maxDepth = 0
maxId = 0

class Node():
    def __init__(self, leftSide, rightSide, parent, action, depth):
        global maxDepth, maxId
        self.leftSide = leftSide
        self.rightSide = rightSide
        self.parent = parent
        self.action = action
        self.depth = depth
        maxId += 1
        print maxId
        #if self.depth > maxDepth:
            #print "currentDepth = %d" % self.depth
            #print "number of nodes = %d" % self.id
            #maxDepth += 1

class Result():
    def __init__(self, startSide, endSide, action, endBoatSide):
        startSide[0] = startSide[0] - action[0]
        startSide[1] = startSide[1] - action[1]
        endSide[0] = endSide[0] + action[0]
        endSide[1] = endSide[1] + action[1]
        if endBoatSide == "right":
            self.rightSide = endSide
            self.leftSide = startSide
            self.rightSide[2] = 1
            self.leftSide[2] = 0
        else:
            self.rightSide = startSide
            self.leftSide = endSide
            self.rightSide[2] = 0
            self.leftSide[2] = 1
        self.action = action

def uninformedSearch(initialNode, goalNode, fringe):
    closedList = set()
    fringe.put(initialNode)
    while True:
        if fringe.empty():
            sys.exit("No solution found!")
        currentNode = fringe.get()
        if goalTest(currentNode, goalNode):
            return currentNode
        if not inClosedList(currentNode, closedList):
            closedList.add(currentNode)
            map(fringe.put, expand(currentNode))

def inClosedList(node, closedList):
    for x in closedList:
        if (node.leftSide == x.leftSide) and (node.rightSide == x.rightSide):
            return True
    return False

def expand(node):
    successors = set()
    for result in successor_fn(node):
        newNode = Node(result.leftSide, result.rightSide, node, result.action, node.depth + 1)
        successors.add(newNode)
    return successors

def goalTest(node, goalNode):
    if (node.leftSide == goalNode.leftSide) and (node.rightSide == goalNode.rightSide):
        return True
    else:
        return False

def successor_fn(node):
    global possibleActions
    allowedActions = filter(lambda x: testAction(x, node), possibleActions)
    results = map(lambda y: applyAction(y, node), allowedActions)
    return results

def applyAction(action, node):
    if node.rightSide[2] == 1:
        result = Result(list(node.rightSide), list(node.leftSide), action, "left")
    else:
        result = Result(list(node.leftSide), list(node.rightSide), action, "right")
    return result

def testAction(action, node):
    if node.rightSide[2] == 1:
        startSide = list(node.rightSide)
        endSide = list(node.leftSide)
    else:
        startSide = list(node.leftSide)
        endSide = list(node.rightSide)

    startSide[0] = startSide[0] - action[0]
    startSide[1] = startSide[1] - action[1]
    endSide[0] = endSide[0] + action[0]
    endSide[1] = endSide[1] + action[1]

    if (startSide[0] < 0) or (startSide[1] < 0) or (endSide[0] < 0) or (endSide[1] < 0):
        return False
    elif ((startSide[0] == 0) or (startSide[0] >= startSide[1])) and (endSide[0] == 0 or (endSide[0] >= endSide[1])):
        return True
    else:
        return False

def getNodePath(node):
    currentNode = node
    pathToNode = []
    while True:
        try:
            if currentNode.parent == None:
                break
            pathToNode.append(currentNode.action)
        except:
            break
        currentNode = currentNode.parent

    return pathToNode[::-1]

def getStateFromFile(file):
    with open(file) as f:
        content = f.readlines()
    return Node(map(int, content[0].strip('\n').split(',')), map(int, content[1].strip('\n').split(',')), None, None, 0)

def outputStateToFile(file, state):
    f = open(file, 'w')
    f.write(str(state.leftSide)[1:-1].replace("'", "").replace(" ", ""))
    f.write('\n')
    f.write(str(state.rightSide)[1:-1].replace("'", "").replace(" ", ""))
    f.close()

def printState(state):
    print str(state.leftSide)[1:-1].replace(" ", "")
    print str(state.rightSide)[1:-1].replace(" ", "")

def main():
    initialState = getStateFromFile(initialStateFile)
    goalState    = getStateFromFile(goalStateFile)

    # Choose data structure based on mode
    if mode == "bfs":
        fringe = Queue.Queue()
    elif (mode == "dfs") or (mode == "iddfs"):
        fringe = Queue.LifoQueue()
    else:
        sys.exit('Selected mode not supported')

    resultNode = uninformedSearch(initialState, goalState, fringe)

    outputStateToFile(outputFile, initialState)
    print getNodePath(resultNode)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        sys.exit('Incorrect number of arguments:\n<initial> <goal> <mode> <output>')
    initialStateFile = sys.argv[1]
    goalStateFile    = sys.argv[2]
    mode             = sys.argv[3]
    outputFile       = sys.argv[4]
    main()
