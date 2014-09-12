import hashlib

class MyNode:	
	nodeCount = 0
	# N = 

	def __init__(self, ipAddress):
		#b = MyNode.b
		MyNode.nodeCount += 1

		#self.routingTable = [[None for x in xrange(2**b)] for x in xrange(32)] 
		#self.leafSet = [None for x in xrange(2**(b+1))]
		#self.neighborhoodSet = [None for x in xrange(2**b)]
		
		self.routingTable = [[]]
		self.lowLeafSet = []
		self.UpLeafSet = []
		self.neighborhoodSet = []

		self.ipAddress = ipAddress

		temp = str(ipAddress)
		temp = temp.encode('utf-8')
		self.nodeKey = hashlib.md5(temp).hexdigest()
		
	def __str__(self):
		return self.nodeKey
	
	def __del__(self):
		'''print "Deleting: " + str(self)'''

