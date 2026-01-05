import simpy
import numpy as np
import random
import math

from .position import Position
from .traits import *

class Food:
    def __init__(self, age, position: Position, traits: FoodTraits, simulation: "Simulation"):
        self.age = age
        
        self.position = position
        
        self.traits = traits

        self.simulation = simulation
        self.simulation.validatePosition(self.position)

        self.live = self.simulation.env.process(self.live())

        # Place food in the world grid
        self.simulation.world.place(self, self.position)


    def tick(self):
        self.age += 1


    def live(self):
        while True:
            self.tick()
            if(self.age >= self.traits.totalLifespan):
                break
            yield self.simulation.env.timeout(1)


    def getStage(self):
        for stage, (start, end) in self.traits.stageDurations.items():
            if start <= self.age < end:
                return stage
                
        return FoodStage.ROTTEN


    def getNutrition(self):
        stage = self.getStage()
        return self.traits.nutritionalValue[stage]
