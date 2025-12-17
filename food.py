import simpy
import numpy as np
import random
import math

from position import Position

class Food:
    def __init__(self, age, position: Position, traits: FoodTraits):
        self.age = age
        
        self.position = position
        
        self.traits = traits