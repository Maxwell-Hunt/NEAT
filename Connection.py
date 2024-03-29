from random import random

class Connection:
    # Initialize Connection
    def __init__(self,fromNode,toNode,innovationNumber):
        self.fromNode = fromNode # ID number
        self.toNode = toNode # ID number
        self.innovationNumber = innovationNumber # Historical Marking
        self.weight = random() * 4 - 2 # Decides how much the connection will be valued
        self.enabled = True # Decides whether the gene is enabled



    def print(self):
        print(str(self.fromNode) + " " + str(self.toNode) + " " + str(self.weight) + " " + str(self.enabled))
    # Creates an exact copy of the original connection
    def copy(self):
        c = Connection(self.fromNode,self.toNode,self.innovationNumber)
        c.weight = self.weight
        c.enabled = self.enabled
        return c
