import operations
import helper
import random
from node import MyNode
from constants import nodes

A = MyNode(helper.generateIpAddress())
X = MyNode(helper.generateIpAddress())
operations.route(A, X)

def addNewNode():
    # Getting random existing node - assuming it's a nearby pastry node
    if(len(nodes) != 0):
        i = random.randint(0, len(nodes)-1)
        A = nodes[i]
    else:
        # No existing node present
        A = None
    
    # Randomly generating a new node
    X = MyNode(helper.generateIpAddress())
    r = operations.add_node(A, X)
    if(r != -1):
        print "node: " + str(X) + "added successfully"