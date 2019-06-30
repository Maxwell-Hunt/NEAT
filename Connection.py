from random import random;

class Connection:
    # Initialize Connection
    def __init__(self,fromNode,toNode,innovationNumber):
        self.fromNode = fromNode; # ID number
        self.toNode = toNode; # ID number
        self.innovationNumber = innovationNumber; # Historical Marking
        self.weight = random() * 2 - 1; # Decides how much the connection will be valued
        self.enabled = True; # Decides whether the gene is enabled


    # Creates an exact copy of the original connection
    def copy(self):
        c = Connection(self.fromNode,self.toNode,self.innovationNumber);
        c.weight = self.weight;
        c.enabled = self.enabled;
        return c;
