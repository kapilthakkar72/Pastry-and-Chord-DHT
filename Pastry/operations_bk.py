import helper
from constants import nodes, neighborSetLen, lowLeafSetLen, \
	upLeafSetLen

'''A : Existing node
...X : New node'''
from helper import isNodeAlive, getMinLeaf, getMaxLeaf, getRelativeDistance, \
	getNumericDistance, getClosestNode, getMinDistNode, printNode,\
	isEligibleDownLeaf, isEligibleUpLeaf

def add_node(X):
	# Getting the neighbors
	A = helper.getClosestNode(nodes, X)
	
	if(A and A.nodeKey == X.nodeKey):
		print "node already present-- " + str(X)
		return -1

	
	# Nothing to be done if it's the first node
	if(A == None):
		nodes.append(X)
		return

	routePath = route(A, X)	
	X.routePath = routePath

	Z = routePath[-1]
	
	nodes.append(X)
	
	updateRoutingTable(A, X, routePath)
	updateNeighborSet(A, X)
	updateLeafSet(Z, X)
	
	# Sending state to other nodes
	updateOthers(X)
	
def updateRoutingTable(A, X, routePath):
	for B in routePath:
		j = -1
		prefixLen = helper.shl(B.nodeKey, X.nodeKey)
		for t_node in B.routingTable[prefixLen]:
			j += 1
			if j == int(X.nodeKey[prefixLen], 16):
				continue
			X.routingTable[prefixLen][j] = t_node

def updateNeighborSet(A, X):
	X.neighborhoodSet.append(A)
	
	for node in A.neighborhoodSet:
		if len(X.neighborhoodSet) == neighborSetLen:
			break
		X.neighborhoodSet.append(node)

def updateLeafSet(Z, X):
	# Adding Z to the leafSet
	if(isEligibleUpLeaf(Z, X)):
		X.upLeafSet.append(Z)
	elif(isEligibleDownLeaf(Z, X)):
		X.downLeafSet.append(Z)
		
	# Taking leafSet from Z
	t_leafSet = Z.downLeafSet + Z.upLeafSet
	for t_leaf in t_leafSet:
		if(len(X.downLeafSet) < lowLeafSetLen and isEligibleDownLeaf(t_leaf, X)):
				X.downLeafSet.append(t_leaf)
		if(len(X.upLeafSet) < upLeafSetLen and isEligibleUpLeaf(t_leaf, X)):
				X.upLeafSet.append(t_leaf)

def updateOthers(X):
	t_nodes = X.neighborhoodSet + X.upLeafSet + X.downLeafSet
	
	for routeTableRow in X.routingTable:
		for routeTableEntry in routeTableRow:
			if(isNodeAlive(routeTableEntry)):
				t_nodes.append(routeTableEntry)
				
	t_nodes = list(set(t_nodes))

	# Updating neighborhoodSet of others
	for otherNode in t_nodes:
		# adding X into the neighborhoodSet of otherNode if not enough neighbors
		if(len(otherNode.neighborhoodSet) < neighborSetLen):
			otherNode.neighborhoodSet.append(X)
			break
		# replacing neighbor of otherNode with X if more closer
		for neighborOfOtherNode in otherNode.neighborhoodSet:
			if(getRelativeDistance(neighborOfOtherNode, otherNode) > getRelativeDistance(X, otherNode)):
				otherNode.neighborhoodSet.remove(neighborOfOtherNode)
				otherNode.neighborhoodSet.append(X)
				break


	# updating leafs of others
	for otherNode in t_nodes:
		# adding X into the leafSet of leaf if not enough leafs
		if(len(otherNode.downLeafSet) < lowLeafSetLen and isEligibleDownLeaf(X, otherNode)):
				otherNode.downLeafSet.append(X)
				break
		elif(len(otherNode.upLeafSet) < upLeafSetLen and isEligibleUpLeaf(X, otherNode)):
				otherNode.upLeafSet.append(X)
				break
		
		# replacing leaf of otherNode with X if more numerically closer
		t_leafOfOtherNodeSet = otherNode.downLeafSet + otherNode.upLeafSet
		for leafOfOtherNode in t_leafOfOtherNodeSet:
			if leafOfOtherNode in otherNode.downLeafSet and X.nodeKey < otherNode.nodeKey:
				if(getNumericDistance(leafOfOtherNode, otherNode) > getNumericDistance(X, otherNode)):
					otherNode.downLeafSet.remove(leafOfOtherNode)
					otherNode.downLeafSet.append(X)
					break
			if leafOfOtherNode in otherNode.upLeafSet and X.nodeKey > otherNode.nodeKey:
				if(getNumericDistance(leafOfOtherNode, otherNode) > getNumericDistance(X, otherNode)):
					otherNode.upLeafSet.remove(leafOfOtherNode)
					otherNode.upLeafSet.append(X)
					break


	# updating nodes in routing table with X
	for otherNode in t_nodes:
		prefixLen = helper.shl(otherNode.nodeKey, X.nodeKey)
		row = prefixLen
		col = int(X.nodeKey[prefixLen], 16)
		routeTableEntry = otherNode.routingTable[row][col]
		if not(isNodeAlive(routeTableEntry)):
			otherNode.routingTable[row][col] = X

def route(A, X):	
	routePath = []
	while(1):
		
		routePath.append(A)
		if len(routePath) > 20:
			print "route path too much"
		
		# returning if found the node
		if A.nodeKey == X.nodeKey:
			return routePath
		
		# search in leafSet
		leafSet = A.downLeafSet + A.upLeafSet
		if leafSet:  # checking if the leafSet is not empty
			
			minLeaf = getMinLeaf(A)
			if minLeaf is None:
				minLeaf = A
				
			maxLeaf = getMaxLeaf(A)
			if maxLeaf is None:
				maxLeaf = A
				
			if(minLeaf.nodeKey <= X.nodeKey <= maxLeaf.nodeKey):
				leafSet.append(A)  # Adding the currentNode in the leafSet...currentNode can be nearest
				nearestleaf = getMinDistNode(leafSet, X)
				
				# no need to append the routePath if nearestLeaf is the current node
				'''if A.nodeKey != nearestleaf.nodeKey:
					routePath.append(nearestleaf)
					
				return routePath'''
				
				if A.nodeKey == nearestleaf.nodeKey:
					return routePath
				
				A = nearestleaf
				continue

		# search in routing table
		prefixLen = helper.shl(A.nodeKey, X.nodeKey)
		row = prefixLen
		col = int(X.nodeKey[prefixLen], 16)
		distFromA = helper.getNumericDistance(A, X)
		routeTableEntry = A.routingTable[row][col]
		if(isNodeAlive(routeTableEntry)):
			A = routeTableEntry
			continue  # forwarded to the closer node
		else:
			# repair the routingTableEntry
			'''repairRouteTableEntry(A, row, col)'''  # commented here since handled in the deletion
			# Send to numerically closer node
			t_list = A.downLeafSet + A.upLeafSet + A.neighborhoodSet
			for rowEntry in A.routingTable[row]:
				if(isNodeAlive(rowEntry)):
					t_list.append(rowEntry)
			t_list = list(set(t_list))
			
			for node in t_list:
				t_prefixLen = helper.shl(node.nodeKey, X.nodeKey)
				t_dist = helper.getNumericDistance(node, X)
				if(t_prefixLen >= prefixLen and t_dist < distFromA):
					A = node
					break
		
		# returning if no node more near to the last node in the routePath
		if routePath[-1].nodeKey == A.nodeKey:
			return routePath
		
	return routePath
	
def repairRouteTableEntry(A, row, col):
	# asking nodes in the same row for replacement node
	for r in range(row, len(A.routingTable)):
		for c in range(0, len(A.routingTable[r])):
			t_node = A.routingTable[r][c]
			if(c != col and isNodeAlive(t_node)):
				t_node_routeTableEntry = t_node.routingTable[row][col]
				if(isNodeAlive(t_node_routeTableEntry)):
					A.routingTable[row][col] = t_node_routeTableEntry
					return

# Iterating over all the nodes in the network & repairing the failed entry 
def nodeDeleted(X):
	X.isNodeActive = False
	for node in nodes:
		# Repair leaf set
		if X in node.upLeafSet:
			node.upLeafSet.remove(X)
			temp = getMaxLeaf(node)
			
			if temp:
				t_leafSet = temp.downLeafSet + temp.upLeafSet
				for leaf in t_leafSet:
					if isEligibleUpLeaf(leaf, node) and leaf not in node.upLeafSet and isNodeAlive(leaf):
						node.upLeafSet.append(leaf)
						break

		elif X in node.downLeafSet:
			node.downLeafSet.remove(X)
			temp = getMinLeaf(node)
			
			if temp:
				t_leafSet = temp.downLeafSet + temp.upLeafSet
				for leaf in t_leafSet:
					if isEligibleDownLeaf(leaf, node) and leaf not in node.downLeafSet and isNodeAlive(leaf):
						node.downLeafSet.append(leaf)
						break
				
		# Repair neighborhood set
		if X in node.neighborhoodSet:
			node.neighborhoodSet.remove(X)
			t_neighborOfNeighborList = []
			# getting all the neighbor of neighbors
			for neighbor in node.neighborhoodSet:
				if(isNodeAlive(neighbor)):
					t_neighborOfNeighborList += neighbor.neighborhoodSet
			
			t_neighborOfNeighborList = list(set(t_neighborOfNeighborList))
			while t_neighborOfNeighborList:
				closestNeighborOfNeighbor = getClosestNode(t_neighborOfNeighborList, node)
				
				if(closestNeighborOfNeighbor.nodeKey == node.nodeKey):
					t_neighborOfNeighborList.remove(closestNeighborOfNeighbor)
					continue
				
				node.neighborhoodSet.append(closestNeighborOfNeighbor)
				break
		
		# Repair routing table
		for routeTableRow in node.routingTable:
			try:
				if X in routeTableRow:
					row = node.routingTable.index(routeTableRow)
					col = routeTableRow.index(X)
					repairRouteTableEntry(node, row, col)
					break
			except ValueError:
				continue
		
			
