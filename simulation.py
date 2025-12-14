import simpy
import numpy as np
import random
import math

from organism import Organism
from traits import Traits
from position import Position
from food import Food

class Simulation:
    def __init__(self, worldsize):
        self.env = simpy.Environment()
        self.worldSize = worldsize
        self.world = self.initWorld()
        self.organismList = []
        self.childCounter ={}


    def initWorld(self):
        world = np.empty((self.worldSize, self.worldSize), dtype=object)
        world.fill(None)
        numPoints = (self.worldSize * self.worldSize) // 800  # approx 1 every 800 spaces

        # pick random coordinates
        xs = np.random.randint(0, self.worldSize, numPoints)
        ys = np.random.randint(0, self.worldSize, numPoints)
        world[xs, ys] = Food(pos=Position(x=xs, y=ys), nutritionValue=random.randint(40,60))

        return world


    def mate(self, parent1, parent2):
        parent1.energy = max(parent1.energy - parent1.energyCapacity//3, 0)
        parent2.energy = max(parent2.energy - parent2.energyCapacity//3, 0)

        generation = max(parent1.generation, parent2.generation) + 1
        if generation not in parent1.sim.childCounter:
            parent1.sim.childCounter[generation] = 0
        parent1.sim.childCounter[generation] += 1
        childName = "Gen" + str(generation) + "_" + str(parent1.sim.childCounter[generation])

        childTraits = Traits(
            detectionRadius = (parent1.detectionRadius + parent2.detectionRadius) // 2 + 2*random.randint(-1,1),
            speed = (parent1.speed + parent2.speed) //2 + 1*random.randint(-1,1),
            energy = (parent1.energyCapacity //3 + parent2.energyCapacity //3) // 2, #takse a third of parents' energy capacity
            energyCapacity = (parent1.energyCapacity + parent2.energyCapacity) // 2 + 10*random.randint(-1,1),
            slowDownAge = (parent1.slowDownAge + parent2.slowDownAge) // 2 + 3*random.randint(-1,1),
            reproductionAge = (parent1.reproductionAge + parent2.reproductionAge) // 2 + 1*random.randint(-1,1),
            matingCallRadius = (parent1.matingCallRadius + parent2.matingCallRadius) // 2 + 10*random.randint(-1,1),
            generation = generation
        )

        
        child = Organism(
            name = childName, 
            species = "Lion", 
            age = 0, 
            position = Position(
                x = (parent1.position.x + parent2.position.x) // 2,
                y = (parent1.position.y + parent2.position.y) // 2
            ),
            traits = childTraits,
            sim = parent1.sim
        )
        print(f"{parent1.name} and {parent2.name} have mated to produce {child.name} (Gen {child.generation})")
        parent1.sim.organismList.append(child)


    def run(self, ticks):
        self.env.run(until=ticks)