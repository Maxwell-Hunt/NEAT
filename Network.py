from Node import Node;
from random import random;
from Connection import Connection;
import math;

class Network:
    def __init__(self,numInputs,numOutputs):
        self.numInputs = numInputs;
        self.numOutputs = numOutputs;
        self.fitness = 0;
        self.species = 0;
        self.nodes = [];
        self.connections = [];
        self.rank = "normal";

        # Creates Input and Output Nodes
        for i in range(numInputs + numOutputs + 1):
            if(i < numInputs + 1):
                self.nodes.append(Node(i,"input"));
            else:
                self.nodes.append(Node(i,"output"));

    def getNodeIndex(self,number):
        for i in range(len(self.nodes)):
            if(self.nodes[i].number == number):
                return i;
        return -1;

    def connectNodes(self):
        for connection in self.connections:
            self.nodes[self.getNodeIndex(connection.toNode)].inputConnections.append(connection.copy());

    def allEngaged(self):
        for node in self.nodes:
            if not node.engaged:
                return False;
        return True;

    # shifts the connections weight values
    def mutateShiftConnection(self,mr,ss):
        for i in range(len(self.connections)):
            if(random() < mr):
                self.connections[i].weight += random() * ss * 2 - ss;

    # gives connections new weight values
    def mutateRandomConnection(self,mr):
        for i in range(len(self.connections)):
            if(random() < mr):
                self.connections[i].weight = random() * 2 - 1;

    # disables or enables random genes
    def mutateEnableDisable(self,mr):
        for i in range(len(self.connections)):
            if(random() < mr):
                if(self.connections[i].enabled):
                    self.connections[i].enabled = False;
                else:
                    self.connections[i].enabled = True;

    # Creates a Connection between 2 nodes
    def mutateAddConnection(self,mr,history):
        if(random() < mr):
            node1 = self.nodes[math.floor(random() * len(self.nodes))];
            node2 = self.nodes[math.floor(random() * len(self.nodes))];
            exists = False;
            self.connectNodes();
            for i in range(1000):
                if(not node1.isConnectedTo(node2.number,self)):
                    if(node1.type == "input" and node2.type == "hidden"):
                        break;
                    if(node1.type == "input" and node2.type == "output"):
                        break;
                    if(node1.type == "hidden" and node2.type == "output"):
                        break;
                    if(node1.type == "hidden" and node2.type == "hidden"):
                        break;
                node1 = self.nodes[math.floor(random() * len(self.nodes))];
                node2 = self.nodes[math.floor(random() * len(self.nodes))];
                if(i == 999):
                    exists = True;


            for connection in self.connections:
                if(connection.fromNode == node1.number and connection.toNode == node2.number):
                    exists = True;


            if(exists == False):
                con = Connection(node1,node2,0);
                innovationNumber = history.add(node1.number,node2.number);
                self.connections.append(Connection(node1.number,node2.number,innovationNumber));


            for node in self.nodes:
                node.inputConnections = [];

    def mutateAddNode(self,mr,history):
        if(random() < mr):
            connectionIndex = math.floor(random() * len(self.connections));
            self.connections[connectionIndex].enabled = False;
            newNode = Node(self.nodes[len(self.nodes) - 1].number + 1,"hidden")
            self.nodes.append(newNode);

            fNode = self.connections[connectionIndex].fromNode;
            tNode = newNode.number;
            inno = history.add(fNode,tNode);
            con = Connection(fNode,tNode,inno);
            con.weight = 1;
            self.connections.append(con);

            fNode = newNode.number;
            tNode = self.connections[connectionIndex].toNode;
            inno = history.add(fNode,tNode);
            con = Connection(fNode,tNode,inno);
            con.weight = self.connections[connectionIndex].weight;
            self.connections.append(con);

    @staticmethod
    def crossover(parentA,parentB):
        # In this function we always assume parent A has higher or equal fitness
        child = Network(parentA.numInputs,parentB.numOutputs);

        # Get child's node genes
        child.nodes = [];
        for node in parentA.nodes:
            child.nodes.append(node.copy());

        # Get child's connection genes
        for i in range(len(parentA.connections)):
            exists = False;
            for j in range(len(parentB.connections)):
                if(parentB.connections[j].innovationNumber == parentA.connections[i].innovationNumber):
                    exists = True;
                    if(random() < 0.5):
                        child.connections.append(parentA.connections[i].copy());
                    else:
                        child.connections.append(parentB.connections[j].copy());
                    break;
            if(exists == False):
                child.connections.append(parentA.connections[i].copy());
        return child;

    @staticmethod
    def getAverageWeightDiff(a,b):
        # In this function we assume a is the bigger genome
        s = 0;
        t = 0;
        for i in range(len(a.connections)):
            for j in range(len(b.connections)):
                if(a.connections[i].innovationNumber == b.connections[j].innovationNumber):
                    s += abs(a.connections[i].weight - b.connections[j].weight);
                    t += 1;
                    break;
        if(t != 0):
            s = s / t;
        return s;

    @staticmethod
    def getExcessDisjointGenes(a,b):
        # For this function to work a must be the bigger genome
        t = 0;
        for i in range(len(a.connections)):
            exists = False;
            for j in range(len(b.connections)):
                if(a.connections[i].innovationNumber == b.connections[j].innovationNumber):
                    exists = True;
            if not exists:
                t += 1;
        return t;

    @staticmethod
    def getDistance(a,b,c1,c2):
        N = 0;
        if(len(a.connections) > len(b.connections)):
            N = len(a.connections);
        else:
            N = len(b.connections);

        ED = Network.getExcessDisjointGenes(a,b);
        W = Network.getAverageWeightDiff(a,b);
        if(N > 20):
            return (ED/N) * c1 + W * c2;
        else:
            return ED*c1 + W*c2;

    def feedForward(self,inputs):
        self.connectNodes();
        for i in range(self.numInputs):
            self.nodes[i].value = inputs[i];
        self.nodes[len(inputs)].value = 1;
        count = 0;

        while not self.allEngaged():
            for node in self.nodes:
                if(node.ready(self) and node.engaged == False):
                    node.engage(self);
            count += 1;
            if(count > 10000):
                adadfsa();

        outputs = [];
        for i in range(self.numInputs + 1,self.numInputs + 1 + self.numOutputs):
            outputs.append(self.nodes[i].value);

        for node in self.nodes:
            node.value = 0;
            node.engaged = False;
            node.inputConnections = [];
            node.ouptutConnections = [];
        return outputs;

    def copy(self):
        co = Network(self.numInputs,self.numOutputs);
        co.nodes = [];
        for node in self.nodes:
            co.nodes.append(node.copy());
        for connection in self.connections:
            co.connections.append(connection.copy());
        co.fitness = self.fitness;
        co.species = self.species;
        return co;
        






































