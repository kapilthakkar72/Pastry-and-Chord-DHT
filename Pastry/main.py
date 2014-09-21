import helper
from node import MyNode
from constants import nodes
import operations
import random
from helper import isNodeAlive
import time
from math import ceil,log
import constants

''''A = MyNode(helper.generateIpAddress())
X = MyNode(helper.generateIpAddress())
operations_bk.route(A, X)'''

def addNewNode():
    # Randomly generating a new node
    X = MyNode(helper.generateIpAddress())
    # print "coordinates: " + str(X.coordinates)
    r = operations.add_node(X)
    
    return len(X.routePath)
    # if(r != -1):
        # print "node: " + str(X) + " - added successfully"
    
    
    

def lookUp(S, D):
    return operations.route(S, D)

def silentDeleteNode(X):
    operations.silentDelete(X)
    

def noisyDeleteNode(X):
    return operations.noisyDelete(X)

def getRandomNode():
    while(1):
        randomNode = nodes[random.randint(0, len(nodes) - 1)]
        if isNodeAlive(randomNode):
            return randomNode
    

def addNodes(N):
    routePathLen = []
    for i in range (0, N):
        r = addNewNode()
        routePathLen.append(r)
        # printNodes()
        if i % 100 == 0:
            print ("reached: " + str(i))
    
    avgHops = getAvg(routePathLen)        
    print ("avg hops: " + str(avgHops))
    
    
def lookUpsGetHops(N):
    failCount = 0
    routePathLen = []

    for i in range (0, N):
        if i % 1000 == 0:
            print ("reached: " + str(i))
        A = getRandomNode()
        X = getRandomNode()
        routePath, accessArr = lookUp(A, X)

        if routePath[-1].nodeKey != X.nodeKey:
            failCount += 1
        else:
            routePathLen.append(len(routePath))
            
    
    # print ("going from " + str(A) + " to " + str(X))
    # print ("routePath: ")
    # helper.plist(routePath)

    print ("failCount: " + str(failCount))
    
    avgHops = getAvg(routePathLen)        
    print ("avg hops: " + str(avgHops))
    
            
def lookUpsGetAccesses(N):
    leafAccess = 0
    leafSuccess = 0
    routeAccess = 0
    routeSuccess = 0
    neighborAccess = 0
    neighborSuccess = 0

    for i in range (0, N):
        if i % 1000 == 0:
            print ("reached: " + str(i))
        A = getRandomNode()
        X = getRandomNode()
        routePath, accessArr = lookUp(A, X)
        leafAccess += accessArr[0]
        leafSuccess += accessArr[1]
        routeAccess += accessArr[2]
        routeSuccess += accessArr[3]
        neighborAccess += accessArr[4]
        neighborSuccess += accessArr[5]
        
    
    avgLeafAccess = leafAccess / N
    avgRouteAccess = routeAccess / N
    avgNeighborAccess = neighborAccess / N
        
    percentLeafSuccess = (leafSuccess / leafAccess) * 100
    percentRouteSuccess = (routeSuccess / routeAccess) * 100
    percentNeighborSuccess = 0
    if(neighborAccess != 0):
        percentNeighborSuccess = (neighborSuccess / neighborAccess) * 100
    
    print ("avgLeafAccess: " + str(avgLeafAccess))
    print ("avgRouteAccess: " + str(avgRouteAccess))
    print ("avgNeighborAccess: " + str(avgNeighborAccess))
    print ("percentLeafSuccess: " + str(percentLeafSuccess))
    print ("percentRouteSuccess: " + str(percentRouteSuccess))
    print ("percentNeighborSuccess: " + str(percentNeighborSuccess))
  
    
def getAvg(t_list):
    count = len(t_list)
    total = 0
    
    for element in t_list:
        total += element
    
    return total / count


def silentDeleteNodes(N):
    for i in range(1, 10):
        if i % 10 == 0:
            print ("silentDeleteNodes | reached: " + str(i))
        X = getRandomNode()
        silentDeleteNode(X)
        
def noisyDeleteNodes(N):
    affectCountList = []
    for i in range(1, 10):
        if i % 10 == 0:
            print ("noisyDeleteNodes | reached: " + str(i))
        X = getRandomNode()
        affectCountList.append(noisyDeleteNode(X))
    
    avgAffected = getAvg(affectCountList)
    print ("avgAffected: " + str(avgAffected))
    
def getAvgRouteTableOccupancy():
    occupancyList = []
    occupancyListOther = []
    entriesShallBeFilled = ceil(log(len(nodes),16))*16
    totalEntries= 32*16
    for node in nodes:
        occupiedCnt = 0
        for routeTableRow in node.routingTable:
            for routeTableEntry in routeTableRow:
                if routeTableEntry:
                    occupiedCnt += 1
        
        occupancy = (occupiedCnt-32)/entriesShallBeFilled
        occupancyList.append(occupancy)
        
        occupancyOther = (occupiedCnt-32)/totalEntries
        occupancyListOther.append(occupancyOther)
        
    avgOccupancy = getAvg(occupancyList)
    print ("Avg occupancy: " + str(avgOccupancy*100))
    
    avgOccupancyOther = getAvg(occupancyListOther)
    print ("Avg occupancy other: " + str(avgOccupancyOther*100))


# silentDeleteNodes(500)
# start = time.time()

addNodes(7500)
getAvgRouteTableOccupancy()
#noisyDeleteNodes(20)
# lookUpsGetHops(100000)


# end = time.time()
# print ("time: " + str(int(end-start)))
print ("here")
# silentDeleteNodes(50)
# lookUps(200000)   
