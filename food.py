import simpy
import numpy as np
import random
import math

from position import Position

class Food:
    def __init__(self, position: Position, traits: FoodTraits):
        self.position = position

        self.nutritionValue = traits.nutritionValue
        self.slowDownAge = traits.slowDownAge
        self.generation = traits.generation