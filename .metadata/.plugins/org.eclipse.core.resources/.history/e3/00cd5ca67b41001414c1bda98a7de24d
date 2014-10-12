import hashlib
import random
from constants import b
from urllib3.connectionpool import xrange

class MyNode:	

	id = 0
	
	def __init__(self, ipAddress):
		#b = MyNode.b

		self.routingTable = [[None for x in xrange(2**b)] for x in xrange(32)]
		#self.leafSet = [None for x in xrange(2**(b+1))]
		#self.neighborhoodSet = [None for x in xrange(2**b)]
		
		#self.routingTable = []
		self.downLeafSet = []
		self.upLeafSet = []
		self.neighborhoodSet = []
		self.isNodeActive = True

		self.ipAddress = ipAddress
		self.coordinates = [random.randint(0,1000), random.randint(0,1000)]

		temp = str(ipAddress)
		temp = temp.encode('utf-8')
		self.nodeKey = hashlib.md5(temp).hexdigest()
		
		MyNode.id += 1
		self.id = MyNode.id
		self.routePath = []
		
	def __str__(self):
		return str(self.id) + " : " + str(self.nodeKey)
	
	'''
	def __del__(self):
		''''''print "Deleting: " + str(self)'''''''
	'''
