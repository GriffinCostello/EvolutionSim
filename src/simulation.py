import simpy
import random

from collections import defaultdict
from .organism import Organism
from .traits import *
from .position import Position
from .food import Food
from .world import World
from .statistics import Statistics

class Simulation:
    def __init__(self, worldsize):
        self.env = simpy.Environment()
        self.worldSize = worldsize
        self.world = World(worldsize, self)
        self.statistics = Statistics()

        #Global variables 
        self.organismList = []
        self.organismChildCounter = {}
        self.stopEvent = self.env.event()

        self.env.process(self.systemTick())

        numFood = (self.worldSize*self.worldSize) // 300 #one food every 300 places
        self.world.placeInitialFood(numFood)


    def run(self, ticks):
        self.env.run(
            until=simpy.events.AnyOf(self.env, [self.stopEvent, self.env.timeout(ticks)])
        )


    def systemTick(self):
        while True:
            yield self.env.timeout(1)

    
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
            traits = parent1.traits.inheritOrganismTraits(parent1.traits, parent2.traits, generation),
            simulation = parent1.simulation
        )
        if isinstance(child.traits, HerbivoreTraits):
            for traitName, value in vars(child.traits).items():
                if traitName != "generation":
                    self.statistics.logTraits(traitName, child.traits.generation, value)
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