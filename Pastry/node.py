import hashlib

class MyNode:
	b = 4
	nodeCount = 0
	# N = 

	def __init__(self, ipAddress):
		b = MyNode.b
		MyNode.nodeCount += 1

		self.routingTable = [[None for x in xrange(2**b)] for x in xrange(32)] 
		self.leafSetSmaller = [None for x in xrange(2**b)]
		self.leafSetLarger = [None for x in xrange(2**b)]
		self.neighborhoodSet = [None for x in xrange(2**b)]

		self.ipAddress = ipAddress

		temp = str(ipAddress)
		temp = temp.encode('utf-8')
		self.nodeKey = hashlib.md5(temp).hexdigest()

