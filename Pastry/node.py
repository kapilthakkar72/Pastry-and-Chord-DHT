import hashlib
import math

class Node:
	b = 4
	nodeCount = 0
	#N = 

	def __init__(self, ipAddress):
		Node.nodeCount ++

		self.routingTable = [[None for x in xrange(2**b)] for x in xrange(32)] 
		self.leafSetSmaller = [None for 2**(b)]
		self.leafSetLarger = [None for 2**(b)]
		self.neighborhoodSet = [None for 2**(b+1)]

		self.ipAddress = ipAddress

		temp = str(ipAddress)
        temp = temp.encode('utf-8')
        self.hashKey = hashlib.md5(temp).hexdigest()
        
