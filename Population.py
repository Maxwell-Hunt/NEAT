from History import History
from Species import Species
from Network import Network
from math import *
from random import *

class Population:
    def __init__(self,agent,popSize,gaurenteedElitism=91,interSpeciesBreeding=0.001,initialComplexity=0,fitnessGoal=100,initiallyConnected=False,stepSize=0.3,MRGeneral=0.8,MRShift=0.9,MRRandom=0.1,MREnableDisable=0.01,MRAddNode=0.03,MRAddConnection=0.05,c1=1,c2=0.4,requiredDistance=3,maxStaleness=15):
        self.popSize = popSize
        self.agentType = agent
        self.history = History()
        self.agents = []
        self.children = []
        self.networks = []
        self.species = []
        self.speciesPool = []
        self.bestOverTime = []
        self.avgOverTime = []
        self.speciesOverTime = []
        self.generation = 0
        self.bestFit = 0
        self.avgFit = 0
        self.champ = None
        self.solution = None
        self.c1 = c1
        self.c2 = c2
        self.mrGeneral = MRGeneral
        self.mrShift = MRShift
        self.stepSize = stepSize
        self.mrRandom = MRRandom
        self.mrEnableDisable = MREnableDisable
        self.mrAddNode = MRAddNode
        self.mrAddConnection = MRAddConnection
        self.requiredDistance = requiredDistance
        self.initiallyConnected = initiallyConnected
        self.initialComplexity = initialComplexity
        self.fitnessGoal = fitnessGoal
        self.interSpeciesBreeding = interSpeciesBreeding
        self.gaurenteedElitism = gaurenteedElitism

        for i in range(self.popSize):
            self.agents.append(agent())
            self.networks.append(self.agents[i].brain)
            self.networks[i].mutateAddConnection(1,self.history)
            for j in range(self.initialComplexity):
                self.networks[i].mutateAddNode(1,self.history)
            if(self.initiallyConnected):
                for j in range(100):
                    self.networks[i].mutateAddConnection(1,self.history)

    def plot(self):
        import matplotlib.pyplot as plt
        plt.plot(range(len(self.bestOverTime)),self.bestOverTime)
        plt.plot(range(len(self.avgOverTime)),self.avgOverTime)
        plt.plot(range(len(self.speciesOverTime)),self.speciesOverTime)
        plt.show()

    def createSpeciesPool(self):
        for species in self.species:
            for _ in range(ceil(species.totalFitness) * 25):
                self.speciesPool.append(species)

    def getSpecies(self):
        #return self.speciesPool[floor(random() * len(self.speciesPool))]
        return choice(self.speciesPool)

    def updateStatistics(self):
        best = 0
        avg = 0
        cha = None
        for network in self.networks:
            avg += network.fitness
            if(network.fitness > best):
                best = network.fitness
                cha = network
        self.bestFit = best
        self.avgFit = avg/len(self.networks)
        self.bestOverTime.append(self.bestFit)
        self.avgOverTime.append(self.avgFit)
        self.speciesOverTime.append(len(self.species))
        self.champ = cha
        if(self.bestFit > self.fitnessGoal):
            self.solution = self.champ

    def removeStale(self):
        i = len(self.species) - 1
        while(i >= 0):
            if(self.species[i].staleness > 15):
                print("---------------")
                print("Species Deleted")
                print("---------------")
                for network in self.species[i].networks:
                    network.fitness = 0
                del self.species[i]
            i -= 1

    def speciate(self):
        for i in range(len(self.networks)):
            speciesFound = False
            for j in range(len(self.species)):
                dist = None
                if(len(self.networks[i].connections) > len(self.species[j].mascot.connections)):
                    dist = Network.getDistance(self.networks[i],self.species[j].mascot,self.c1,self.c2)
                else:
                    dist = Network.getDistance(self.species[j].mascot,self.networks[i],self.c1,self.c2)
                if(dist < self.requiredDistance):
                    self.species[j].networks.append(self.networks[i])
                    speciesFound = True
                    break
            if(speciesFound == False):
                newSpecies = Species(self.networks[i])
                newSpecies.networks.append(self.networks[i])
                self.species.append(newSpecies)

        # Delete extinct species
        i = len(self.species) - 1
        while(i >= 0):
            if(len(self.species[i].networks) < 1):
                print("---------------")
                print("Species Deleted")
                print("---------------")
                del self.species[i]
            i -= 1       

        for i in range(len(self.species)):
            for network in self.species[i].networks:
                network.species = i

    def adjustFits(self):
        for species in self.species:
            for network in species.networks:
                adjustedFitness = network.fitness / len(species.networks)
                network.fitness = adjustedFitness
                species.totalFitness += network.fitness

    def elitism(self):
        self.children = []
        for species in self.species:
            species.sort()
            if(len(species.networks) < 5):
                net = species.networks[0].copy()
                net.rank = "master"
                self.children.append(net)

    def breedNextGen(self):
        self.createSpeciesPool()
        
        while len(self.children) < self.popSize:
            s = self.getSpecies()
            if(s.matingpool == []):
                s.createMatingpool()
            if(random() > self.interSpeciesBreeding):
                parentA = s.getNetwork()
                parentB = s.getNetwork()
            else:
                parentA = choice(self.networks)
                parentB = choice(self.networks)
            child = None
            if(parentA.fitness > parentB.fitness):
                child = Network.crossover(parentA,parentB)
            else:
                child = Network.crossover(parentB,parentA)
            if(random() < self.mrGeneral):
                child.mutateShiftConnection(self.mrShift,self.stepSize)
                child.mutateRandomConnection(self.mrRandom)
            child.mutateAddNode(self.mrAddNode,self.history)
            child.mutateAddConnection(self.mrAddConnection,self.history)
            child.mutateEnableDisable(self.mrEnableDisable)
            self.children.append(child)

    def reset(self):
        self.speciesPool = []
        for network in self.children:
            network.fitness = 0
            network.species = 0

        for species in self.species:
            species.networks = []
            species.matingpool = []
            species.totalFitness = 0

        self.networks = self.children
        for i in range(len(self.agents)):
            self.agents[i] = self.agentType(self.networks[i])
        self.children = []

    def run(self):
        for agent in self.agents:
            agent.update()
        

    def evaluate(self):
        # Update solutions and best networks
        self.updateStatistics()



        # Delete Stale Species
        self.removeStale()

        

        # Place networks into species
        self.speciate()




        # Adjust fitness scores
        self.adjustFits()
        
        
        



        

        # Place best of each species into next generation and render the lowest performers infertile
        self.elitism()


        




        # Breed the rest of the next generation
        self.breedNextGen()

        # Reset
        self.reset()
        
    




























