import simpy
import numpy as np
import random
import math

from position import Position

class Food:
    def __init__(self, pos: Position, nutritionValue):
        self.pos = pos
        self.nutritionValue = nutritionValue