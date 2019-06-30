from Connection import Connection;
from Activations import *;

class Node:
    # Initialize Node
    def __init__(self,number,type,layer=1,activation=sigmoid):
        self.number = number;
        self.type = type; 
        self.inputConnections = [];
        self.activation = activation; 
        self.value = 0;
        self.layer = layer; 
        self.engaged = False;

    def ready(self,network):
        for con in self.inputConnections:
            if(network.nodes[network.getNodeIndex(con.fromNode)].engaged == False):
                return False;
        return True;
    
    def isConnectedTo(self,other,network):
        if(self.number == other):
            return True;
        for con in self.inputConnections:
            if(network.nodes[network.getNodeIndex(con.fromNode)].isConnectedTo(other,network)):
                return True;
        return False;
    
    def engage(self,network):
        self.engaged = True;
        for con in self.inputConnections:
            self.value += network.nodes[network.getNodeIndex(con.fromNode)].value * con.weight;
        if(self.type != "input"):
            self.value = self.activation(self.value);

    def copy(self):
        n = Node(self.number,self.type,activation=self.activation);
        n.value = self.value;

        for inputConnection in self.inputConnections:          
            n.inputConnections.append(inputConnection.copy());

        return n; 

