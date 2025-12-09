import time
import sys
import matplotlib.pyplot as plt

class Point:
    x:float
    y:float
    z:float

class BoundedCountingPriorityQueue:
    # Group ID / amount
    elementToSize:list[int]
    sortedElements:list[int] = []
    nbMaxElements:int = 3
    
    def push(self, group:int):
        for k in range(len(self.sortedElements)):
            if self.sortedElements[k] == group:
                return
        
        lastIndex = len(self.sortedElements) - 1
        i = lastIndex
        # Binary search would be faster, but not with small arrays
        while (i != -1 and self.elementToSize[self.sortedElements[i]] < self.elementToSize[group]):
            i -= 1
        
        # if i != -1 and i <= lastIndex and group == self.sortedElements[i]:
        #     return
        
        i += 1
        if i >= self.nbMaxElements:
            return
        
        if i > lastIndex:
            self.sortedElements.append(group)
            return
        
        # insertion
        for j in range(lastIndex, i, -1):
            self.sortedElements[j] = self.sortedElements[j - 1]
            
        self.sortedElements[i] = group

# dist1 < dist2
# dist1*dist1 < dist2*dist2
# keeping the result squared to prevent sqrt() (opti)
def sqrDist(p1:Point, p2:Point) -> float:
    xDelta = p1.x - p2.x 
    yDelta = p1.y - p2.y
    zDelta = p1.z - p2.z
    return xDelta * xDelta + yDelta * yDelta + zDelta * zDelta

# Parsing: O(n)
def parseInput(content:str) -> list[Point]:
    points:list[Point] = []
    lines = content.splitlines()
    for line in lines:
        xStr, yStr, zStr = line.split(',')
        point = Point()
        point.x = float(xStr)
        point.y = float(yStr)
        point.z = float(zStr)
        points.append(point)
    return points

def day8(content:str):
    points:list[Point] = parseInput(content)
    nbPoints = len(points)

    # O(n)
    # setup disjoint union set
    pointToGroup:list[int] = [0] * nbPoints
    groupToSize:list[int] = [0] * nbPoints
    closestSqrDist:list[float] = [sys.float_info.max] * nbPoints
    for i in range(nbPoints):
        pointToGroup[i] = i
    
    def getGroup(i:int) -> int:
        # inverse ackermann complexity
        while (pointToGroup[i] != pointToGroup[pointToGroup[i]]):
            pointToGroup[i] = pointToGroup[pointToGroup[i]]
        return pointToGroup[i]
    
    for i in range(nbPoints):
        connectedPointIndex = i
        for j in range(i+1, nbPoints):
            # if (i == j):
            #     continue
            dist = sqrDist(points[i], points[j])
            if (dist < closestSqrDist[i]):
                closestSqrDist[i] = dist
                connectedPointIndex = j
        
        if (dist < closestSqrDist[j]):
            closestSqrDist[connectedPointIndex] = dist
            pointToGroup[connectedPointIndex] = connectedPointIndex
            
        pointToGroup[i] = getGroup(connectedPointIndex)
    
    priorityQueue = BoundedCountingPriorityQueue()
    priorityQueue.elementToSize = groupToSize
    
    for i in range(nbPoints):
        group = getGroup(i)
        groupToSize[group] += 1
        priorityQueue.push(group)
    
    return groupToSize[priorityQueue.sortedElements[0]]\
        * groupToSize[priorityQueue.sortedElements[1]]\
        * groupToSize[priorityQueue.sortedElements[2]]

class DisjointUnionSet:
    idToGroup:list[int]
    
    def __init__(self, size):
        self.idToGroup = list(range(size))
    
    def getGroup(self, i:int) -> int:
        group = self.idToGroup[i]
        while (group != self.idToGroup[group]):
            group = self.idToGroup[group]
        self.idToGroup[i] = group
        return group
    
    def setDirectGroup(self, iFrom:int, iTo:int):
        self.idToGroup[iFrom] = iTo
    
    def setGroup(self, iFrom:int, iTo:int):
        self.setDirectGroup(iFrom, self.getGroup(iTo))
    
    def merge(self, i, j):
        self.setGroup(self.getGroup(i), j) 

def findClosestNaive(points:list[Point]):
    nbPoints = len(points)
    pointToClosestPoint:list[int] = [0] * nbPoints
    for i in range(nbPoints):
        closestSqrDist = sys.float_info.max
        for j in range(nbPoints):
            if i == j:
                continue
            
            squareDist = sqrDist(points[i], points[j])
            
            if squareDist < closestSqrDist:
                closestSqrDist = squareDist
                pointToClosestPoint[i] = j
                
    return pointToClosestPoint

def findClosestOptiWithoutSpatialPartionning(points:list[Point]):
    nbPoints = len(points)
    closestSqrDist:list[float] = [sys.float_info.max] * nbPoints
    pointToClosestPoint:list[int] = [0] * nbPoints
    for i in range(nbPoints):
        for j in range(i + 1, nbPoints):
            squareDist = sqrDist(points[i], points[j])
            
            if squareDist < closestSqrDist[i]:
                closestSqrDist[i] = squareDist
                pointToClosestPoint[i] = j
            
            if squareDist < closestSqrDist[j]:
                closestSqrDist[j] = squareDist
                pointToClosestPoint[j] = i
                
    return pointToClosestPoint, closestSqrDist

def day8_1(content:str):
    # Correct
    points:list[Point] = parseInput(content)
    nbPoints = len(points)
    
    # Correct
    pointToClosestPoint, closestSqrDist = findClosestOptiWithoutSpatialPartionning(points)
    pointToClosestPointNaive:list[int] = findClosestNaive(points)
    for i in range(nbPoints):
        assert(pointToClosestPoint[i] == pointToClosestPointNaive[i])
    
    # Correct
    sortedPoints:list[int] = list(range(nbPoints))
    # TODO : C++ nth_element
    sortedPoints.sort(key=lambda index: closestSqrDist[index])
    
    for i in range(1, nbPoints):
        assert(closestSqrDist[pointToClosestPoint[sortedPoints[i]]] != closestSqrDist[sortedPoints[i]]\
            or sortedPoints[i] == pointToClosestPoint[pointToClosestPoint[sortedPoints[i]]])
        assert(closestSqrDist[sortedPoints[i-1]] <= closestSqrDist[sortedPoints[i]])
    
    figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1, projection="3d")
    xList = [p.x for p in points]
    yList = [p.y for p in points]
    zList = [p.z for p in points]
    axes.scatter(xList,yList,zList, c="r", marker="o")
    for x, y, z, i in zip(xList, yList, zList, range(nbPoints)):
        axes.text(x,y,z,i)

    
    for i in range(17):
        pIndex = sortedPoints[i]
        fromPos = points[pIndex]
        toPos = points[pointToClosestPoint[pIndex]]
        axes.plot([fromPos.x, toPos.x], [fromPos.y, toPos.y], [fromPos.z, toPos.z])
    
    groupToSize = [1] * nbPoints
    priorityQueue = BoundedCountingPriorityQueue()
    priorityQueue.elementToSize = groupToSize
    
    disjointUnionSet = DisjointUnionSet(nbPoints)
    # nbIterations = 10
    # nbIterations = 1000
    # for i in range(nbIterations):
    #     pIndex = sortedPoints[i]
    #     disjointUnionSet.setGroup(pIndex, pointToClosestPoint[pIndex])
    
    connectionsLeft = 11
    for i in range(nbPoints):
        pIndex = sortedPoints[i]
        disjointUnionSet.setGroup(pIndex, pointToClosestPoint[pIndex])
        group = disjointUnionSet.getGroup(pIndex)
        assert(group == disjointUnionSet.getGroup(pointToClosestPoint[pIndex]))
        if group != pIndex:
            nbCurrentConnections = groupToSize[pIndex]
            groupToSize[pIndex] = 0
            groupToSize[group] += nbCurrentConnections
            priorityQueue.push(group)
            # fromPos = points[pIndex]
            # toPos = points[group]
            # axes.plot([fromPos.x, toPos.x], [fromPos.y, toPos.y], [fromPos.z, toPos.z])
            connectionsLeft -= 1
            if (connectionsLeft == 0):
                break
            
    plt.show(block=False)
    
    # for i in range(nbPoints):
    #     group = disjointUnionSet.getGroup(i)
    #     neighborGroup = disjointUnionSet.getGroup(pointToClosestPoint[i])
    #     assert(group == neighborGroup)
    
    return groupToSize[priorityQueue.sortedElements[0]]\
        * groupToSize[priorityQueue.sortedElements[1]]\
        * groupToSize[priorityQueue.sortedElements[2]]

def findClosestOptiWithoutSpatialPartionning(points:list[Point]):
    nbPoints = len(points)
    closestSqrDist:list[float] = [sys.float_info.max] * nbPoints
    pointToClosestPoint:list[int] = [0] * nbPoints
    for i in range(nbPoints):
        for j in range(i + 1, nbPoints):
            squareDist = sqrDist(points[i], points[j])
            
            if squareDist < closestSqrDist[i]:
                closestSqrDist[i] = squareDist
                pointToClosestPoint[i] = j
            
            if squareDist < closestSqrDist[j]:
                closestSqrDist[j] = squareDist
                pointToClosestPoint[j] = i
                
    return pointToClosestPoint, closestSqrDist

# OPTIMIZED FINAL
def day8_1_1_1(content:str, nbIterations = 1000, hasPlot:bool = False):
    # Correct
    points:list[Point] = parseInput(content)
    nbPoints = len(points)
    
    connections:list[(int, int, float)] = []
    
    for i in range(nbPoints):
        for j in range(i + 1, nbPoints):
            connections.append((i, j, sqrDist(points[i], points[j])))
    
    connections.sort(key=lambda x: x[2])
    
    disjointUnionSet = DisjointUnionSet(nbPoints)
    for i in range(nbIterations):
        connection = connections[i]
        disjointUnionSet.merge(connection[0], connection[1])
    
    groupToSize = [0] * nbPoints
    priorityQueue = BoundedCountingPriorityQueue()
    priorityQueue.elementToSize = groupToSize

    for i in range(nbPoints):
        group = disjointUnionSet.getGroup(i)
        groupToSize[group] += 1
        priorityQueue.push(group)
            
    return groupToSize[priorityQueue.sortedElements[0]]\
        * groupToSize[priorityQueue.sortedElements[1]]\
        * groupToSize[priorityQueue.sortedElements[2]]
        
        
        
    
# solution: 122430
def day8_1_1(content:str, nbIterations = 1000, hasPlot:bool = False):
    # Correct
    points:list[Point] = parseInput(content)
    nbPoints = len(points)
    
    if hasPlot:
        figure = plt.figure()
        axes = figure.add_subplot(1, 1, 1, projection="3d")
        xList = [p.x for p in points]
        yList = [p.y for p in points]
        zList = [p.z for p in points]
        axes.scatter(xList,yList,zList, c="r", marker="o")
        for x, y, z, i in zip(xList, yList, zList, range(nbPoints)):
            axes.text(x,y,z,i)
    
    disjointUnionSet = DisjointUnionSet(nbPoints)
    pointToClosestPoint:list[int] = [0] * nbPoints
    pointToConnectedPoints = []
    for i in range(nbPoints):
        pointToConnectedPoints.append(set())
    
    def isConnectedTo(p1:int, p2:int) -> bool:
        pMin = min(p1, p2)
        pMax = max(p1, p2)
        return pMax in pointToConnectedPoints[pMin]
        
    def connect(p1:int, p2:int) -> bool:
        pMin = min(p1, p2)
        pMax = max(p1, p2)
        pointToConnectedPoints[pMin].add(pMax)
    
    for k in range(nbIterations):
        if k % 5 == 0:
            print(k)
        closestSqrDist:list[float] = [sys.float_info.max] * nbPoints
        for i in range(nbPoints):
            for j in range(i + 1, nbPoints):
                # if  disjointUnionSet.getGroup(i) != disjointUnionSet.getGroup(j):
                if not(isConnectedTo(i, j)):
                    squareDist = sqrDist(points[i], points[j])
                    if squareDist < closestSqrDist[i]:
                        closestSqrDist[i] = squareDist
                        pointToClosestPoint[i] = j
                    
                    if squareDist < closestSqrDist[j]:
                        closestSqrDist[j] = squareDist
                        pointToClosestPoint[j] = i

        minSqrDist = sys.float_info.max
        pIndex = 0
        for i in range(nbPoints):
            if closestSqrDist[i] < minSqrDist:
                minSqrDist = closestSqrDist[i]
                pIndex = i

        connect(pIndex, pointToClosestPoint[pIndex])
        disjointUnionSet.merge(pIndex, pointToClosestPoint[pIndex])
        
        if hasPlot:
            fromPos = points[pIndex]
            toPos = points[pointToClosestPoint[pIndex]]
            axes.plot([fromPos.x, toPos.x], [fromPos.y, toPos.y], [fromPos.z, toPos.z])
    
    if hasPlot:
        plt.show(block=False)
    
    groupToSize = [0] * nbPoints
    priorityQueue = BoundedCountingPriorityQueue()
    priorityQueue.elementToSize = groupToSize

    for i in range(nbPoints):
        group = disjointUnionSet.getGroup(i)
        groupToSize[group] += 1
        priorityQueue.push(group)
            
    return groupToSize[priorityQueue.sortedElements[0]]\
        * groupToSize[priorityQueue.sortedElements[1]]\
        * groupToSize[priorityQueue.sortedElements[2]]





# OPTIMIZED FINAL
def day8_2(content:str):
    # Correct
    points:list[Point] = parseInput(content)
    nbPoints = len(points)
    
    connections:list[(int, int, float)] = []
    
    for i in range(nbPoints):
        for j in range(i + 1, nbPoints):
            connections.append((i, j, sqrDist(points[i], points[j])))
    
    connections.sort(key=lambda x: x[2])
    
    start = time.time_ns()
    
    breakOnLastMerge:bool = True
    
    if not(breakOnLastMerge): # 390776600ns
        disjointUnionSet = DisjointUnionSet(nbPoints)
        result = None
        for i in range(len(connections)):
            connection = connections[i]
            g1 = disjointUnionSet.getGroup(connection[0])
            g2 = disjointUnionSet.getGroup(connection[1])
            if g1 != g2:
                result = points[connection[0]].x * points[connection[1]].x
            disjointUnionSet.merge(connection[0], connection[1])
            
        end = time.time_ns()
        print("duration: ", end - start)
        
        return result
    
    else: # 4747700ns
        # optimized with size buffer
        groupToSize = [1] * nbPoints
        disjointUnionSet = DisjointUnionSet(nbPoints)
        result = None
        for i in range(len(connections)):
            connection = connections[i]
            p1 = connection[0]
            p2 = connection[1]
            group1 = disjointUnionSet.getGroup(p1)
            group2 = disjointUnionSet.getGroup(p2)
            
            # manual merge
            group1Size = groupToSize[group1]
            groupToSize[group2] += group1Size
            disjointUnionSet.setDirectGroup(group1, group2)
            groupToSize[group1] -= group1Size
            if groupToSize[group2] == nbPoints:
                result = points[p1].x * points[p2].x
                break
        
        end = time.time_ns()
        print("duration: ", end - start)
        
    return result



filepath = "day8/input.txt"
content:str
try:
    with open(filepath) as file:
        content = file.read() 
except Exception as e:
    print("couldnt open file: ", e)

# start = time.time_ns()
# result = day8_1_1_1(content)
result = day8_2(content)
# end = time.time_ns()
# print("duration: ", end - start)
print(result)

