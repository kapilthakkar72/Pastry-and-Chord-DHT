import KTsChord
import random
from time import time

nodes=4000
no_of_messages=nodes*2
m=16

network = KTsChord.Network()

#n = network.add_node(0) #create node and join network
#n1 = network.add_node(1) #create node and join network
#n2 = network.add_node(3) #create node and join network
#n3 = network.add_node(7) #create node and join network

performDeleteAfter=0

nodesDeleted=0

additionTimeInitial=time()

#Let's Create a Large network...

for i in range(0,nodes):
    n=network.add_node()
    print("Node Number: "+ str(i+1))
    print("Node is :" + str(n.id))
    #print("Successor: "+ str(n.finger[1].id))
    #print("Predecessor: " + str(n.predecessor.id))
    #print("Finger Table:")
    #for j in range(1,m+1):
    #    print("Start - "+ str((n.id +2**(j-1))% 2**m) + " Node - "+str(n.finger[j].id))
    print("\n")
    '''
    performDeleteAfter=performDeleteAfter+1

    if  performDeleteAfter==25:
        network.delete_node(network.get_random_node_from_netwrok().id)
        performDeleteAfter=0
        nodesDeleted=nodesDeleted+1
        pass
    '''   
messages=[]

additionTimeFinal=time()

nodesDeleted=0
deletionTimeInitial=time()

for i in range(1,int(nodes*20/100)):
    network.delete_node(network.get_random_node_from_netwrok().id)
    nodesDeleted=nodesDeleted+1

deletionTimeFinal=time()


## Let's go for message passing
for i in range(0,no_of_messages):
    #print("Message: "+ str(i))
    start_node=network.get_random_node_from_netwrok()
    message=KTsChord.Message(start_node, random.randint(0,2**m -1));
    start_node.find_successor(0,0,message);
    messages.append(message);

total_length=0
min_length=111110
max_length=0

list_of_hops=[]

for i in range(0,no_of_messages):
    #total_length=total_length+messages[i].hops
    #if(min_length > messages[i].hops):
    #    min_length = messages[i].hops
        
    #if(max_length < messages[i].hops):
    #    max_length = messages[i].hops
    list_of_hops.append(messages[i].hops)
    #print("Message Number "+ str(i+1) + " Source:" + str(messages[i].source.id) + " Destination:" + str(messages[i].destination) + " Path length: "+ str(messages[i].hops));

list_of_hops.sort()
KTsChord.additionHops.sort()
KTsChord.deletionHops.sort()

#print(list_of_hops);

start=int(len(list_of_hops)/100);
count=0;

for i in range(start,len(list_of_hops)-start):
    total_length=total_length+list_of_hops[i]
    if(min_length > list_of_hops[i]):
        min_length = list_of_hops[i]
       
    if(max_length < list_of_hops[i]):
        max_length = list_of_hops[i]
    count=count+1


print(KTsChord.additionHops)
print(KTsChord.deletionHops)

newAddList=[]
start=int(len(KTsChord.additionHops)/100);

for i in range(start,len(KTsChord.additionHops)-start):
    newAddList.append(KTsChord.additionHops[i])


newDeleteList=[]
start=int(len(KTsChord.deletionHops)/100);

for i in range(start,len(KTsChord.deletionHops)-start):
    newDeleteList.append(KTsChord.deletionHops[i])


print("")
print("Total Nodes: "+str(nodes))
print("Average length of msg: "+ str(total_length / count))
print("Maximum Length of msg: "+ str(max_length))
print("Minimum Length of msg: "+ str(min_length))
print("")
print("Nodes Deeleted: "+str(nodesDeleted))
print("Max path of node deleted.. "+str(max(newDeleteList)))
print("Min path of node added.. "+str(min(newDeleteList)))
print("Average path of node deleted.."+str(sum(newDeleteList)/len(newDeleteList)))
print("")
print("Nodes Added: "+str(nodes))
print("Max path of node Added.. "+str(max(newAddList)))
print("Min path of node Added.. "+str(min(newAddList)))
print("Average path of node Added.."+str(sum(newAddList)/len(newAddList)))
print("")
print("Time To add "+str(nodes)+" is: "+str(additionTimeFinal-additionTimeInitial))
print("Time To delete "+str(nodesDeleted)+" is: "+str(deletionTimeFinal-deletionTimeInitial))
print("So avg time to add : "+ str((additionTimeFinal-additionTimeInitial)/nodes))
print("So avg time to delete : "+ str((deletionTimeFinal-deletionTimeInitial)/nodesDeleted))