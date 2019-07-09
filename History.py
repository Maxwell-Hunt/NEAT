from Connection import Connection

class History:
    def __init__(self):
        self.globalConnections = []
        self.maxInno = 0

    # Adds to global connections if the connection given doesn't already exist.  Also returns the innovation number the connection should get
    def add(self,fromNode,toNode):
        if(len(self.globalConnections) > 0):
            exists = False
            innovationNumber = self.globalConnections[len(self.globalConnections) - 1].innovationNumber + 1
            for connection in self.globalConnections:
                if(connection.fromNode == fromNode and connection.toNode == toNode):
                    innovationNumber = connection.innovationNumber
                    exists = True
                    break
            if(exists == False):
                self.globalConnections.append(Connection(fromNode,toNode,innovationNumber))
        
            return innovationNumber
        else:
            self.globalConnections.append(Connection(fromNode,toNode,1))
            return 1
