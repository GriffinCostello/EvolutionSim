import simpy
import numpy as np
import random
import math

from position import Position
from traits import *

class Food:
    def __init__(self, age, position: Position, traits: FoodTraits, simulation: Simulation):
        self.age = age
        
        self.position = position
        
        self.traits = traits

        self.simulation = simulation

        self.live = self.simulation.env.process(self.live())

    def tick(self):
        self.age += 1

    def live(self):
        while True:
            self.tick()
            yield self.simulation.env.timeout(1)