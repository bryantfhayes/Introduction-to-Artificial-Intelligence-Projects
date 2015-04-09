## NOTES AND QUESTIONS ##
# 1) Do I have to empty the clear list each time iddfs increases depth limit?
# 2) SOLVED
# 3) Do we count expanded nodes or popped nodes?
# 4) How is iddfs space complexity O(b*d)
# 5) Is going from 25 nodes expanded to 179 supposed to be good?
# 6) My DFS finds a longer path than BFS?
#
import sys, collections, heapq

# GLOBAL VARIABLES #
initialStateFile  = None
goalStateFile     = None
mode              = None
outputFile        = None
possibleActions   = [[1,0],[2,0],[0,1],[1,1],[0,2]]
depthLimit        = 0
nodeCount         = 0
lastExpansion     = 0
numOfNodesCreated = 0

class Node():
    def __init__(self, leftSide, rightSide, parent, action, depth, pathcost):
        global numOfNodesCreated
        self.leftSide = leftSide
        self.rightSide = rightSide
        self.parent = parent
        self.action = action
        self.depth = depth
        self.pathcost = pathcost
        self.key = tuple(self.leftSide + self.rightSide)
        #print self.key
        numOfNodesCreated += 1


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

    def __len__(self):
        return len(self._queue)

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
    global nodeCount, lastExpansion, depthLimit, numOfNodesCreated
    closedList = {}
    if mode == "a*":
        fringe.push(initialNode, initialNode.pathcost)
    else:
        fringe.append(initialNode)
    while True:
        if len(fringe) == 0:
            # When in iddfs mode, increment depthLimit and restart search
            if mode == "iddfs":
                if depthLimit > 400:
                    exit(1)
                lastExpansion = 0
                fringe.append(initialNode)
                depthLimit += 1
                numOfNodesCreated = 0
                closedList = {}
                if depthLimit % 50 == 0:
                    print depthLimit
                continue
            else:
                sys.exit("No solution found!")
        if mode == "bfs":
            currentNode = fringe.popleft()
        else:
            currentNode = fringe.pop()
        if goalTest(currentNode, goalNode):
            print currentNode.depth
            return currentNode
        if not inClosedList(currentNode, closedList):
            nodeCount += 1
            closedList[currentNode.key] = currentNode.depth
            if mode == "a*":
                map(lambda x: fringe.push(x, x.pathcost), expand(currentNode))
            else:
                map(fringe.append, expand(currentNode))

# TODO: need third constraint for iddfs to get optimal solution
def inClosedList(node, closedList):
    if node.key in closedList:
        if node.depth >= closedList[node.key]:
            return True
    else:
        return False


def expand(node):
    successors = []
    for result in successor_fn(node):
        newNode = Node(result.leftSide, result.rightSide, node, result.action, node.depth + 1, node.depth + 1)
        successors.append(newNode)
    return successors

def goalTest(node, goalNode):
    if (node.leftSide == goalNode.leftSide) and (node.rightSide == goalNode.rightSide):
        return True
    else:
        return False

def successor_fn(node):
    global possibleActions
    if mode == "iddfs":
        if node.depth == depthLimit:
            return []
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
    # Determine which side the boat is on
    if node.rightSide[2] == 1:
        startSide = list(node.rightSide)
        endSide = list(node.leftSide)
    else:
        startSide = list(node.leftSide)
        endSide = list(node.rightSide)
    # Make perform the action and see results
    startSide[0] = startSide[0] - action[0]
    startSide[1] = startSide[1] - action[1]
    endSide[0] = endSide[0] + action[0]
    endSide[1] = endSide[1] + action[1]
    # If results cause more cannibals than missionaires, return false
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
    return Node(map(int, content[0].strip('\n').split(',')), map(int, content[1].strip('\n').split(',')), None, None, 0, 0)

def outputPathToFile(file, path):
    f = open(file, 'w')
    f.write(str(path))
    f.write('\n')
    f.close()

def printState(state):
    print str(state.leftSide)[1:-1].replace(" ", "")
    print str(state.rightSide)[1:-1].replace(" ", "")

def main():
    initialState = getStateFromFile(initialStateFile)
    goalState    = getStateFromFile(goalStateFile)

    # Choose data structure based on mode
    if (mode == "bfs") or (mode == "dfs") or (mode == "iddfs"):
        fringe = collections.deque()
    elif (mode == "a*"):
        fringe = PriorityQueue()
    else:
        sys.exit('Selected mode not supported')

    resultNode = uninformedSearch(initialState, goalState, fringe)

    outputPathToFile(outputFile, getNodePath(resultNode))
    print getNodePath(resultNode)
    print "Expanded %d nodes" % nodeCount
    print "nodes created: %d" % numOfNodesCreated

if __name__ == "__main__":
    if len(sys.argv) < 5:
        sys.exit('Incorrect number of arguments:\n<initial> <goal> <mode> <output>')
    initialStateFile = sys.argv[1]
    goalStateFile    = sys.argv[2]
    mode             = sys.argv[3]
    outputFile       = sys.argv[4]
    main()
