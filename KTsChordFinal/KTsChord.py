import random
import math

# Number of digits to represent a node 
m=16

#Create a Node class

additionHops=[]
deletionHops=[]

class Node:
    
    add=0
    delete=0

    #constructor of class Node    
    list_of_nodes=[]
    
    def __init__(self,node_id):
        self.id = node_id
        self.finger= []
        self.alive=True
        self.secondSuccessor=None;
        for i in range(0,m+1):
            self.finger.append(None);
        self.predecessor=None
        Node.add=0;
        
    def belongsOC (self,a,b,c):
        if(b<c):
            if(b<a<=c):
                return True;
            else:
                return False;
        else:
            if(b==c):
                return True;
            else:
                if(a> b or a<=c):
                    return True;        
        return False;
    
    # a belongs to [b,c)        
    def belongsCO (self,a,b,c):
        if(b<c):
            if(b<=a<c):
                return True;
            else:
                return False;
        else:
            if(b==c):
                return True;
            else:
                if(a>= b or a< c):
                    return True;        
        return False
    
    # a belongs to (b,c)        
    def belongsOO (self,a,b,c):
        if(b<c):
            if(b<a<c):
                return True;
            else:
                return False;
        else:
            if(b==c):
                return True;
            else:
                if(a> b or a< c):
                    return True;        
        return False;
        
    def find_successor(self,node_id,addOrDelete,message=None):
        if(message==None):
            if addOrDelete==0:
                Node.add=Node.add+1;
            else:
                Node.delete=Node.delete+1;

            n_dash=self.find_predecessor(node_id,addOrDelete);
            return n_dash.finger[1];
        else:
            if not self.alive:
                return None
            
            node = self.find_predecessor(0,0,message) #get as close as possible
            if node==None or not node.alive:
                return None

            if node.id == message.destination: #cool we got there
                return node
            else: #almost, teh successor of this one is responsible for that key
                message.route.append(node.finger[1].id)
                message.hops=message.hops+1
                return node.finger[1]
    
    def find_predecessor(self,id,addOrDelete,message=None):
        
        if(message==None):
            n_dash=self;

            if addOrDelete==0:
                Node.add=Node.add+1;
            else:
                Node.delete=Node.delete+1

        
            if(n_dash.finger[1].alive == False):
                n_dash.finger[1]=self.secondSuccessor
                n_dash.secondSuccessor =n_dash.secondSuccessor.finger[1]
                self.stabilize(addOrDelete)
        
            while(not self.belongsOC(id, n_dash.id, n_dash.finger[1].id)):
                n_dash=n_dash.closest_preceding_finger(id);
            return n_dash;
        else:
            if not self.alive:
                return None
            id = message.destination

            if id == self.id:
                return self
 
            node = self                    
            #print "before",node, node.fingers[0]
            while (node.id != node.finger[1].id ) and not self.belongsOC(id, node.id, (node.finger[1].id)):
                node = node.closest_preceding_finger(0,message)    
                if(node==None or not node.alive or node.finger[1] == None):
                   return None
                message.route.append(node.id)
                message.hops=message.hops+1
                #print "inside",node, node.fingers[0]
                if node.id == id:
                   return node
        return node
    
    def closest_preceding_finger(self,id,message=None):
        if(message==None):
            for i in range(m,0,-1):
                if(self.belongsOO(self.finger[i].id,self.id,id)):
                    return self.finger[i];
            return self
        else:
            if not self.alive:
                return None

            id = message.destination
            for i in range(m,0,-1): #loop backwards
                if self.belongsOO(self.finger[i].id,self.id,id):
                    return self.finger[i]
            return self
    
    def join(self,n_dash):        
        Node.list_of_nodes.append(self);
        if(n_dash):
            Node.add=0;
            self.init_finger_table(n_dash,0);
            self.finger[1]=n_dash.find_successor(self.id,0);
            self.stabilize(0);
            additionHops.append(Node.add);
        else:
            Node.add=0;
            for i in range(1,m+1):
                self.finger[i]=self;
            self.predecessor=self;            
            additionHops.append(Node.add);
    
    def init_finger_table(self,n_dash,addOrDelete):
        self.finger[1]=n_dash.find_successor(self.id+1,addOrDelete);
        self.predecessor=self.finger[1].predecessor;
        self.finger[1].predecessor = self;
        
        for i in range(1, m):
            if(self.belongsCO((self.id + (2 ** i))% (2**m), self.id, self.finger[i].id)):
                self.finger[i+1]=self.finger[i];
            else:
                self.finger[i+1]=n_dash.find_successor((self.id + (2 ** i))% (2**m),addOrDelete);
        
    
    def stabilize(self,addOrDelete):        

            print(Node.add)

        #for j in range (0,int(len(Node.list_of_nodes)*0.4)):
            for i in range(0,len(Node.list_of_nodes)):
                n=Node.list_of_nodes[i];
                
                if(n.finger[1].alive==False):
                    n.finger[1]=n.secondSuccessor
                    n.secondSuccessor=n.finger[1].finger[1]
                else:
                    n.secondSuccessor=n.finger[1].finger[1]
                
                x=n.finger[1].predecessor;
                
                if(x.alive == False):
                    n.finger[1].predecessor=None
                
                if(self.belongsOO(x.id, n.id, n.finger[1].id)):
                    if(x.alive==True):
                        n.finger[1]=x;
                n.finger[1].notify(n,addOrDelete);
                n.fix_fingers(addOrDelete);
            
    def notify(self,n_dash,addOrDelete):
        if(self.predecessor == None or self.belongsOO(n_dash.id, self.predecessor.id, self.id)):
            self.predecessor=n_dash;

            if addOrDelete==0:
                Node.add=Node.add+1;
            else:
                Node.delete=Node.delete+1
    
    def fix_fingers(self,addOrDelete):
        for i in range(1,m+1):
            initialAdd=Node.add;
            initialDelete=Node.delete;
            x=self.find_successor((self.id + (2**(i-1)))% (2**m),addOrDelete);
            #self.finger[i]=self.find_successor((self.id + (2**(i-1)))% (2**m),addOrDelete);
            if(self.finger[i]!=x):
                self.finger[i]=x;
            else:
                if(addOrDelete==0):
                    Node.add=initialAdd;
                else:
                    Node.delete=initialDelete;
            
    def remove_from_list(self):
        for i in range(0,len(Node.list_of_nodes)):
            if(Node.list_of_nodes[i].id == self.id):
                return Node.list_of_nodes.pop(i);
            
    def go_off(self):
        Node.delete=0
        self.alive=False
        x=self.remove_from_list()
        self.stabilize(1)
        deletionHops.append(Node.delete);
        
class Network:
    
    #constructor
    
    list_of_nodes=[]
    
    def get_random_node_from_netwrok(self):
        i=random.randint(1,len(Network.list_of_nodes)-1)
        return self.list_of_nodes[i]
    
    def exists(self,id):
        for i in range(0,len(Network.list_of_nodes)):
            if(Network.list_of_nodes[i].id == id):
                return True
        return False
    
    def get_random_id(self):
        random_id=random.randint(1,2**m-1)
        while(1):
            flag=True
            #print("Generating id")
            for i in range(0,len(Network.list_of_nodes)):
                if(Network.list_of_nodes[i].id == random_id):
                    flag=False
                    break;
            if(flag):
                return random_id;
            else:
                random_id=random_id+1
                #random_id=random.randint(1,2**m-1)
    
    def add_node(self,node_id=None):
        if(not node_id):
            node_id=self.get_random_id();
        if(len(Network.list_of_nodes)==0):
            new_node=Node(node_id);
            new_node.join(None);
            Network.list_of_nodes.append(new_node);
            return new_node;
        x=self.exists(node_id);
        if(x):
            print("Node id exists. Can not add this node.");    
        else:
            r_index=random.randrange(0,len(Network.list_of_nodes));
            r_node=Network.list_of_nodes[r_index];
            new_node=Node(node_id);
            new_node.join(r_node);
            Network.list_of_nodes.append(new_node);
            return new_node;
    
    def get_node(self,id):
        for i in range(0,len(Network.list_of_nodes)):
            if(Network.list_of_nodes[i].id == id):
                return Network.list_of_nodes.pop(i);
            
    def delete_node(self,id):
        exist=self.exists(id);
        if(not exist):
            print("Given node does not exist in the network");
        else:
            n=self.get_node(id);
            n.go_off()
            print("Node with node id "+str(id)+" deleted")

    #def calculateKeys

class Message:
    
    def __init__(self,source,destination):
        self.source=source;
        self.destination=destination
        self.hops=0
        self.route = []