import simpy
import numpy as np
import random
import math

from .organism import Organism
from .traits import *
from .position import Position
from .food import Food

class Simulation:
    def __init__(self, worldsize):
        self.env = simpy.Environment()
        self.worldSize = worldsize
        self.world = self.initWorld()

        #Global variables 
        self.organismList = []
        self.organismChildCounter = {}
        self.lifeSpan = [1] #list to keep track of lifespans of dead organisms, base value 1 to prevent division by zero
        self.stopEvent = self.env.event()

        self.env.process(self.systemTick())

        numFood = (self.worldSize*self.worldSize) // 300 #one food every 200 places
        self.placeFood(numFood)


    #Initializes the world as a worldSize * worldSize grid with type objects
    def initWorld(self):
        world = np.empty((self.worldSize, self.worldSize), dtype=object)
        world.fill(None)
        self.world = world
        return self.world


    #places food on the map
    def placeFood(self, numFood):
        for i in range(0,numFood):
            x = random.randint(0, self.worldSize -1)
            y = random.randint(0, self.worldSize -1)
            food = Food(
                age = random.randint(0,50),
                position = Position(
                    x = x, 
                    y = y
                ), 
                traits = FoodTraits(
                    generation = 1,
                    stageConfiguration = {
                        FoodStage.SEED: {"duration": random.randint(7, 10), "nutrition": random.randint(1, 10)},
                        FoodStage.RIPENING: {"duration": random.randint(8, 15), "nutrition": random.randint(15, 25)},
                        FoodStage.RIPE: {"duration": random.randint(18, 25), "nutrition": random.randint(50, 60)},
                        FoodStage.ROTTING: {"duration": random.randint(8, 15), "nutrition": random.randint(20, 25)},
                        FoodStage.ROTTEN: {"duration": random.randint(7, 10), "nutrition": 0},
                    }                   
                ),
                simulation = self
            )


    #Creates a child from two parent organisms
    def mate(self, parent1, parent2):
        if parent1.species != parent2.species:
            return

        if type(parent1.traits) is not type(parent2.traits):
            return

        parent1.energy = max(parent1.energy - parent1.traits.birthEnergy//3, 0)
        parent2.energy = max(parent2.energy - parent2.traits.birthEnergy//3, 0)

        child = self.createChild(parent1, parent2)
        parent1.simulation.organismList.append(child)


    #Create the child object
    def createChild(self, parent1, parent2):
        generation = max(parent1.traits.generation, parent2.traits.generation) + 1
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
            traits = self.inheritOrganismTraits(parent1.traits, parent2.traits, generation),
            simulation = parent1.simulation
        )
        #print(f"{parent1.name} and {parent2.name} have mated to produce {child.name} (Gen {child.traits.generation})")
        return child

    
    #Find's child's generation and number of children in that generation to find Child's Name
    def findChildName(self, parent1, parent2, generation):
        key = (parent1.species, generation)

        if key not in parent1.simulation.organismChildCounter:
            parent1.simulation.organismChildCounter[key] = 0
        parent1.simulation.organismChildCounter[key] += 1

        childName = parent1.species + "_Gen" + str(generation) + "_" + str(parent1.simulation.organismChildCounter[key])
        return childName


    #This calculates the traits of the parents plus slight variation for evolution to occur
    def inheritOrganismTraits(self, traits1, traits2, generation):
        if isinstance(traits1, HerbivoreTraits):
            return HerbivoreTraits(
                detectionRadius = self.inherit((traits1.detectionRadius + traits2.detectionRadius) // 2, 2, 1),
                speed = self.inherit((traits1.speed + traits2.speed) //2, 1, 1),
                energyCapacity = self.inherit((traits1.energyCapacity + traits2.energyCapacity) // 2 , 10, 1),
                birthEnergy = self.inherit((traits1.birthEnergy + traits2.birthEnergy) // 2 , 5, 1),
                slowDownAge = self.inherit((traits1.slowDownAge + traits2.slowDownAge) // 2 , 3, 1),
                reproductionAge = self.inherit((traits1.reproductionAge + traits2.reproductionAge) // 2 , 1, 2),
                matingCallRadius = self.inherit((traits1.matingCallRadius + traits2.matingCallRadius) // 2 , 10, 1),
                digestionTime = self.inherit((traits1.digestionTime + traits2.digestionTime) // 2 , 1, 1),
                generation = generation
            )

        elif isinstance(traits1, CarnivoreTraits):
            return CarnivoreTraits(
                huntingRadius = self.inherit((traits1.huntingRadius + traits2.huntingRadius) // 2, 2, 1),
                speed = self.inherit((traits1.speed + traits2.speed) //2, 1, 1),
                energyCapacity = self.inherit((traits1.energyCapacity + traits2.energyCapacity) // 2 , 10, 1),
                birthEnergy = self.inherit((traits1.birthEnergy + traits2.birthEnergy) // 2 , 5, 1),
                slowDownAge = self.inherit((traits1.slowDownAge + traits2.slowDownAge) // 2 , 3, 1),
                reproductionAge = self.inherit((traits1.reproductionAge + traits2.reproductionAge) // 2 , 1, 2),
                matingCallRadius = self.inherit((traits1.matingCallRadius + traits2.matingCallRadius) // 2 , 10, 1),
                digestionTime = self.inherit((traits1.digestionTime + traits2.digestionTime) // 2 , 1, 1),
                generation = generation
            )
    

    #Helper function for finding variance levels, static since used by whole class, not object instances 
    @staticmethod
    def inherit(value, variance, minimum):
        return max(value + variance*random.randint(-1,1), minimum)


    def run(self, ticks):
        self.env.run(
            until=simpy.events.AnyOf(self.env, [self.stopEvent, self.env.timeout(ticks)])
        )


    def systemTick(self):
        while True:
            yield self.env.timeout(1)

            if self.env.now == 1:
                self.findStats()
            if self.env.now % 100 == 0:
                self.findStats() 


    def findStats(self):
        if len(self.organismList) == 0:
            return
        print("-------------------------------------------------")
        print(f"Number of Organisms Alive {len(self.organismList)}")

        speedTotal = sum(o.traits.speed for o in self.organismList)
        print(f"Speed: {speedTotal / len(self.organismList):.4f}")

        #detectionTotal = sum(o.traits.detectionRadius for o in self.organismList)
       # print(f"Detection Radius: {detectionTotal / len(self.organismList):.4f}")

        energyCapacityTotal = sum(o.traits.energyCapacity for o in self.organismList)
        print(f"Energy Capacity: {energyCapacityTotal / len(self.organismList):.4f}")

        matingCallTotal = sum(o.traits.matingCallRadius for o in self.organismList)
        print(f"Mating Call Radius: {matingCallTotal / len(self.organismList):.4f}")

        slowDownTotal = sum(o.traits.slowDownAge for o in self.organismList)
        print(f"SlowDownAge: {slowDownTotal / len(self.organismList):.4f}")

        reproductionAgeTotal = sum(o.traits.reproductionAge for o in self.organismList)
        print(f"Reproduction Age: {reproductionAgeTotal / len(self.organismList):.4f}")

        birthEnergyTotal = sum(o.traits.birthEnergy for o in self.organismList)
        print(f"Birth Energy: {birthEnergyTotal / len(self.organismList):.4f}")

    
    def validatePosition(self, position: Position):
        if not (0 <= position.x < self.worldSize and 0 <= position.y < self.worldSize):
            raise ValueError("Position out of bounds of the simulation world.")