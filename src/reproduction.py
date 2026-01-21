import simpy
import random

from .position import Position
from .food import Food
from .genetics import *

class Reproduction:
    def __init__(self, organism: "Organism"):
        self.org = organism


    #Creates a child from two parent organisms
    def mate(self, parent2):
        parent1 = self.org

        if parent1.species != parent2.species:
            return

        if type(parent1.genetics) is not type(parent2.genetics):
            return

        parent1.energy = max(parent1.energy - parent1.genetics.birthEnergy//3, 0)
        parent2.energy = max(parent2.energy - parent2.genetics.birthEnergy//3, 0)

        child = self.org.simulation.createChild(parent1, parent2)
        parent1.simulation.organismList.append(child)