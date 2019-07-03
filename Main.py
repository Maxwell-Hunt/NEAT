from Population import Population
from Network import Network
from math import floor



class Player:
    def __init__(self,brain=None):
        self.brain = None
        if(brain == None):
            self.brain = Network(2,1)
        else:
            self.brain = brain

    def update(self):
        self.brain.fitness += self.brain.feedForward([0,1])[0]
        self.brain.fitness += self.brain.feedForward([1,0])[0]
        self.brain.fitness += 1 - self.brain.feedForward([0,0])[0]
        self.brain.fitness += 1 - self.brain.feedForward([1,1])[0]
        self.brain.fitness *= self.brain.fitness
        self.brain.fitness *= 10
            
pop = Population(Player,150,fitnessGoal=120,initiallyConnected=True)

def go():
    pop.run()
    print("--------------")
    print("Running Generation " + str(len(pop.bestOverTime)))
    print("--------------")
    print(pop.bestFit)
    print(pop.avgFit)    
    pop.evaluate()

for i in range(100):
    go()

pop.plot()

