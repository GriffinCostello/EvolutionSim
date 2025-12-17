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
        self.organismList = []
        self.childCounters = {}
        self.env.process(self.regrowFood())


    def initWorld(self):
        world = np.empty((self.worldSize, self.worldSize), dtype=object)
        world.fill(None)
        numFood = (self.worldSize * self.worldSize) // 800
        self.world = world
        self.placeFood(
            numFood = numFood
        )
        return self.world


    def placeFood(self, numFood):
        

        xs = np.random.randint(0, self.worldSize, numFood)
        ys = np.random.randint(0, self.worldSize, numFood)
        for x, y in zip(xs, ys):
            self.world[x, y] = Food(
                Position(x, y), 
                traits = FoodTraits(
                    slowDownAge = 20, 
                    generation = 1, 
                    nutritionValue = random.randint(40, 60)
                )
            )


    def regrowFood(self):
        while True:
            if(self.env.now % 10 ==0):
                self.placeFood(
                    numFood = 50
                )
            yield self.env.timeout(1)


    def mate(self, parent1, parent2):
        if parent1.species is not parent2.species:
            return
        parent1.energy = max(parent1.energy - parent1.traits.energyCapacity//3, 0)
        parent2.energy = max(parent2.energy - parent2.traits.energyCapacity//3, 0)

        generation = max(parent1.traits.generation, parent2.traits.generation) + 1
        key = (parent1.species, generation)
        if key not in parent1.sim.childCounters:
            parent1.sim.childCounters[key] = 0
        parent1.sim.childCounters[key] += 1
        childName = parent1.species + "_Gen" + str(generation) + "_" + str(parent1.sim.childCounters[key])
        
        child = Organism(
            name = childName, 
            species = parent1.species,
            age = 0,
            energy = (parent1.traits.energyCapacity //3 + parent2.traits.energyCapacity //3) // 2, #takse a third of parents' energy capacity
            position = Position(
                x = (parent1.position.x + parent2.position.x) // 2,
                y = (parent1.position.y + parent2.position.y) // 2
            ),
            traits = OrganismTraits(
                detectionRadius = (parent1.traits.detectionRadius + parent2.traits.detectionRadius) // 2 + 2*random.randint(-1,1),
                speed = (parent1.traits.speed + parent2.traits.speed) //2 + 1*random.randint(-1,1),
                energyCapacity = (parent1.traits.energyCapacity + parent2.traits.energyCapacity) // 2 + 10*random.randint(-1,1),
                slowDownAge = (parent1.traits.slowDownAge + parent2.traits.slowDownAge) // 2 + 3*random.randint(-1,1),
                reproductionAge = (parent1.traits.reproductionAge + parent2.traits.reproductionAge) // 2 + 1*random.randint(-1,1),
                matingCallRadius = (parent1.traits.matingCallRadius + parent2.traits.matingCallRadius) // 2 + 10*random.randint(-1,1),
                generation = generation
            ),
            sim = parent1.sim
        )
        print(f"{parent1.name} and {parent2.name} have mated to produce {child.name} (Gen {child.traits.generation})")
        parent1.sim.organismList.append(child)


    def run(self, ticks):
        self.env.run(until=ticks)