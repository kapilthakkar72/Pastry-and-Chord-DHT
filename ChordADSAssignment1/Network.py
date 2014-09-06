import Node


class Network :
    #Number of Digits to represent a key 
    #m= 160
    m=3
    ipaddress = 102168122125
    networkNodes =[]
    
    def create_node(self, node_id):
        n = Node.Node(self.ipaddress,node_id)
        print("Node with id " + str(node_id) + " has node reference number : ")
        print(n)
        if(not self.networkNodes):
            n.join_node(None)
        else:
            n.join_node(self.networkNodes[0])
        self.networkNodes.append(n)
        self.ipaddress= self.ipaddress+1
        return n
    
    