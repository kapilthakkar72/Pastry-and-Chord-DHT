import hashlib
import threading
import random

class Node (threading.Thread):
    
    #m=160
    m=3   
    
    def __init__(self,ipaddress=None,node_id=None):
        threading.Thread.__init__(self)
        self.ipaddress = ipaddress
        temp = str(ipaddress)
        temp = temp.encode('utf-8')
        if (node_id==None):
            self.hashKey=int(hashlib.sha1(temp).hexdigest(),16) % 8
        else:
            self.hashKey=node_id
        self.predecessor=None
        self.successor=None
        self.finger=[]
        self.finger.append([0,0,0])
        for i in range (1,self.m+1):
            self.finger.append([(self.hashKey + 2 ** (i-1)) % (2 ** self.m) , (self.hashKey + 2 ** (i)) % (2 ** self.m), None])
        
    def run(self):
        while(1):
            self.stabilize()
            self.fix_fingers()
            
    def stabilize(self):
        x= self.successor.predecessor
        if(self.belongsOO(x.hashKey, self.hashKey, self.successor.hashKey)):
            self.finger[1][2]=self.successor=x
        self.successor.notify_node(self)
        
    def notify_node(self,n_dash):
        if(self.predecessor == None):
            self.predecessor=n_dash
        elif(self.belongsOO(n_dash.hashKey, self.predecessor.hashKey, self.hashKey)):
            self.predecessor=n_dash
            
    def fix_fingers(self):
        i=random.randrange(2,self.m+1)
        self.finger[i][2]=self.find_successor(self.finger[i][0])
    
    # To find successor of any key key_id   
    def find_successor(self,key_id):
        n_dash = self.find_predecessor(key_id)
        return n_dash.successor
    
    def find_predecessor(self,key_id):
        n_dash=self
        while (1==1):
            if(self.belongsOC(key_id, n_dash.hashKey, n_dash.successor.hashKey)):
                break
            n_dash=n_dash.closest_preceding_finger(key_id);
        return n_dash
    
    def closest_preceding_finger(self,key_id):
        for i in range(self.m,0,-1):
            if(self.finger[i][2] == None):
                continue
            if(self.belongsOO(self.finger[i][2].hashKey, self.hashKey, key_id)):
                return self.finger[i][2] 
        return self
    
    # When any node join_nodes Network
    def join_node(self, n_dash):
        if(n_dash):
            self.predecessor=None
            self.finger[1][2]=self.successor=n_dash.find_successor(self.hashKey)
        else:
            for i in range (1 , self.m+1):
                self.finger[i][2]=self
            self.predecessor=self
            self.successor=self
        self.start()
            
    
    # a belongs to (b,c]        
    def belongsOC (self,a,b,c):
        if(b<c):
            if(b<a<=c):
                return 1;
            else:
                return 0;
        else:
            if(b==c):
                return 1;
            else:
                if(a> b or a<=c):
                    return 1;
        
        return 0;
    
    # a belongs to [b,c)        
    def belongsCO (self,a,b,c):
        if(b<c):
            if(b<=a<c):
                return 1;
            else:
                return 0;
        else:
            if(b==c):
                return 1;
            else:
                if(a>= b or a< c):
                    return 1;
        
        return 0;
    
    # a belongs to (b,c)        
    def belongsOO (self,a,b,c):
        if(b<c):
            if(b<a<c):
                return 1;
            else:
                return 0;
        else:
            if(b==c):
                return 1;
            else:
                if(a> b or a< c):
                    return 1;
        
        return 0;
    
#        if(n_dash):
#            for i in range (1,self.m+1):
#                self.finger.append([(self.hashKey + 2 ** (i-1)) % (2 ** self.m) , (self.hashKey + 2 ** (i)) % (2 ** self.m), None])
#            self.init_finger_table(n_dash)
#            self.successor=self.finger[1][2]
#            self.update_others()
#        else:
#            for i in range (1 , self.m+1):
#                self.finger.append([(self.hashKey + 2 ** (i-1)) % (2 ** self.m) , (self.hashKey + 2 ** (i)) % (2 ** self.m), self])
#            self.predecessor=self
#            self.successor=self
                
#    def init_finger_table(self,n_dash):        
#        self.finger[1][2]=self.successor = n_dash.find_successor(self.finger[1][0])
#       self.predecessor = self.successor.predecessor
#        self.successor.predecessor=self;
#        for i in range (1,self.m):
#            if(self.belongsCO(self.finger[i+1][0], self.hashKey, self.finger[i][2].hashKey)):
#                self.finger[i+1][2]=self.finger[i][2] 
#            else:
#                self.finger[i+1][2]=n_dash.find_successor(self.finger[i+1][0])
                
#    def update_others(self):
#        for i in range (1,self.m+1):
#            p=self.find_predecessor((self.hashKey-2**(i-1)) % (2 ** self.m))
#            p.update_finger_table(self,i)
    
#    def update_finger_table(self,s,i):
#        if(self.belongsCO(s.hashKey, self.hashKey, self.finger[i][2].hashKey)):
#            self.finger[i][2]=s
#            p=self.predecessor
#            p.update_finger_table(s,i)
