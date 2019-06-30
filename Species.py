from operator import attrgetter;
from math import *;
from random import *;

class Species:
    def __init__(self,mascot):
        self.mascot = mascot;
        self.networks = [];
        self.matingpool = [];
        self.staleness = 0;
        self.totalFitness = 0;
        self.bestFit = 0;

    def sort(self):
        sortedNetworks = sorted(self.networks,key=attrgetter("fitness"),reverse=True);
        self.networks = sortedNetworks;
        if(self.networks[0].fitness <= self.bestFit):
            self.staleness += 1;
        else:
            self.staleness = 0;
        self.bestFit = self.networks[0].fitness * len(self.networks);

        i = len(self.networks) - 1;
        while(i >= len(self.networks) - floor(len(self.networks) / 2)):
            self.networks[i].fitness = 0;
            i -= 1;

    def createMatingpool(self):
        for network in self.networks:
            for i in range(ceil(network.fitness * 25)):
                self.matingpool.append(network);

    def getNetwork(self):
        #return self.matingpool[floor(random() * len(self.matingpool))];
        return choice(self.matingpool);
