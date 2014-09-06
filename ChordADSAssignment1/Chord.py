import Network
import time
import sys

# Create node
network = Network.Network()

n = network.create_node(0) #create node and join network
n1 = network.create_node(1) #create node and join network
n2 = network.create_node(3) #create node and join network
n3 = network.create_node(6) #create node and join network

time.sleep(50)

print(n.hashKey)
print(n.successor.hashKey)
print(n.predecessor.hashKey)
print(n.finger)
print("\n")

print(n1.hashKey)
print(n1.successor.hashKey)
print(n1.predecessor.hashKey)
print(n1.finger)
print("\n")

print(n2.hashKey)
print(n2.successor.hashKey)
print(n2.predecessor.hashKey)
print(n2.finger)
print("\n")

print(n3.hashKey)
print(n3.successor.hashKey)
print(n3.predecessor.hashKey)
print(n3.finger)
print("\n")
