import simpy
import numpy as np
import random
import math

from organism import Organism
from traits import *
from position import Position
from food import Food

class Simulation:
    def __init__(self, worldsize):
        self.env = simpy.Environment()
        self.worldSize = worldsize
        self.world = self.initWorld()

        #Global variables 
        self.organismList = []
        self.organismChildCounter = {}

        numFood = (self.worldSize*self.worldSize) // 300 #one food every 300 places
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
            x = random.randint(0, self.worldSize -1), 
            y = random.randint(0, self.worldSize -1)
            self.world[x, y] = Food(
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
        if parent1.species is not parent2.species:
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
            energy = (parent1.traits.energyCapacity //3 + parent2.traits.energyCapacity //3) // 2, #takse a third of parents' energy capacity
            position = Position(
                x = (parent1.position.x + parent2.position.x) // 2,
                y = (parent1.position.y + parent2.position.y) // 2
            ),
            traits = self.inheritTraits(parent1.traits, parent2.traits, generation),
            simulation = parent1.simulation
        )
        print(f"{parent1.name} and {parent2.name} have mated to produce {child.name} (Gen {child.traits.generation})")
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
    def inheritTraits(self, traits1, traits2, generation):
        return OrganismTraits(
            detectionRadius = self.inherit((traits1.detectionRadius + traits2.detectionRadius) // 2, 2),
            speed = self.inherit((traits1.speed + traits2.speed) //2, 1),
            energyCapacity = self.inherit((traits1.energyCapacity + traits2.energyCapacity) // 2 , 10),
            birthEnergy = self.inherit((traits1.birthEnergy + traits2.birthEnergy) // 2 , 5),
            slowDownAge = self.inherit((traits1.slowDownAge + traits2.slowDownAge) // 2 , 3),
            reproductionAge = self.inherit((traits1.reproductionAge + traits2.reproductionAge) // 2 , 1),
            matingCallRadius = self.inherit((traits1.matingCallRadius + traits2.matingCallRadius) // 2 , 10),
            digestionTime = self.inherit((traits1.digestionTime + traits2.digestionTime) // 2 , 1),
            generation = generation
        )
    

    #Helper function for finding variance levels, static since used by whole class, not object instances 
    @staticmethod
    def inherit(value, variance):
        return value + variance*random.randint(-1,1)

    def run(self, ticks):
        self.env.run(until=ticks)