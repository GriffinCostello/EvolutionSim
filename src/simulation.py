import simpy
import random
import time

from collections import defaultdict
from .organism import Organism
from .traits import *
from .position import Position
from .food import Food
from .world import World
from .statistics import Statistics
from .genetics import *

class Simulation:
    def __init__(self, worldsize):
        self.env = simpy.Environment()
        self.worldSize = worldsize
        self.startTime = time.time()

        self.world = World(worldsize, self)
        self.statistics = Statistics()

        #Global variables 
        self.organismList = []
        self.carnivoreList = []
        self.herbivoreList = []
        self.organismChildCounter = {}
        self.stopEvent = self.env.event()

        numFood = (self.worldSize*self.worldSize) // 300 #one food every 300 places
        self.world.placeInitialFood(numFood)


    def run(self, ticks):
        self.ticks = ticks
        self.env.process(self.systemTick())
        self.env.run(
            until=simpy.events.AnyOf(self.env, [self.stopEvent, self.env.timeout(ticks)])
        )


    def systemTick(self):
        remaining = self.ticks
        self.startTime = time.time()
        while True:
            if self.env.now % 100 == 0 and self.env.now != 0:
                if remaining < 0:
                    pass
                else:
                    self.printTime()
                remaining = remaining -100
            yield self.env.timeout(1)

            
    def printTime(self):
        elapsed = time.time()-self.startTime
        minutes = int(elapsed // 60)
        seconds = elapsed % 60
        print(f"\rElapsed Time: {minutes:02d}:{seconds:05.2f} | Organisms: {len(self.organismList):>10} | Herbivores: {len(self.herbivoreList):>10} | Carnivores: {len(self.carnivoreList):>10}", end = "", flush = True)


    #Create the child object
    def createInitialHerbivores(self, i):
        genetics = HerbivoreGenetics(
            foodDetectionRadius = 30,
            predatorDetectionRadius = 10,
            speed = 6,
            energyCapacity = 700,
            birthEnergy = 80,
            slowDownAge = 60,
            reproductionAge = 20,
            matingCallRadius = 200,
            digestionTime = 5,
            generation = 1
        )
        org = Organism(
            name = "Herbivore_Gen1_" + str(i), 
            species = "Herbivore",
            age = random.randint(10, 30),
            energy = random.randint(450,550),
            position = Position(
                x=random.randint(0, self.worldSize-1),
                y=random.randint(0, self.worldSize-1)
            ),
            genetics = genetics,
            simulation = self
        )
        self.organismList.append(org)
        self.herbivoreList.append(org)

        for geneticsName, value in vars(org.genetics).items():
            if geneticsName != "generation":
                self.statistics.logGenetics(geneticsName, org.genetics.generation, value)


    def createInitialCarnivores(self, i):
        genetics = CarnivoreGenetics(
            huntingRadius = 50,
            speed = 8,
            energyCapacity = 500,
            birthEnergy = 80,
            slowDownAge = 60,
            reproductionAge = 20,
            matingCallRadius = 200,
            digestionTime = 5,
            generation = 1
        )
        org = Organism(
            name = "Carnivore_Gen1_" + str(i), 
            species = "Carnivore",
            age = random.randint(10, 30),
            energy = random.randint(350,400),
            position = Position(
                x=random.randint(0, self.worldSize-1),
                y=random.randint(0, self.worldSize-1)
            ),
            genetics = genetics,
            simulation = self
        )
        self.organismList.append(org)
        self.carnivoreList.append(org)
        

    
    #Create the child object
    def createChild(self, parent1, parent2):
        generation = max(parent1.genetics.generation, parent2.genetics.generation) + 1
        childGenetics = parent1.genetics.inheritOrganismGenetics(parent1.genetics, parent2.genetics, generation)
        childName = self.findChildName(parent1, parent2, generation)
        child = Organism(
            name = childName, 
            species = parent1.species,
            age = 0,
            energy = (parent1.traits.birthEnergy + parent2.traits.birthEnergy) // 2, #takse a third of parents' energy capacity
            position = Position(
                x = (parent1.position.x + parent2.position.x) // 2,
                y = (parent1.position.y + parent2.position.y) // 2
            ),
            genetics = childGenetics,
            simulation = parent1.simulation
        )
        if isinstance(child.genetics, HerbivoreGenetics):
            self.herbivoreList.append(child)
            for geneticName, value in vars(child.genetics).items():
                if geneticName != "generation":
                    self.statistics.logGenetics(geneticName, child.genetics.generation, value)
        elif isinstance(child.genetics, CarnivoreGenetics):
            self.carnivoreList.append(child)
        
        self.organismList.append(child)
        return child

    
    #Find's child's generation and number of children in that generation to find Child's Name
    def findChildName(self, parent1, parent2, generation):
        key = (parent1.species, generation)

        if key not in parent1.simulation.organismChildCounter:
            parent1.simulation.organismChildCounter[key] = 0
        parent1.simulation.organismChildCounter[key] += 1

        childName = parent1.species + "_Gen" + str(generation) + "_" + str(parent1.simulation.organismChildCounter[key])
        return childName