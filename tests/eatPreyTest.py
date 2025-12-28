import simpy
import numpy as np
import random
import math
import sys

sys.path.insert(0, "../src")

from simulation import Simulation
from traits import *
from position import Position
from organism import Organism

def main():
    simulation = Simulation(worldsize=10)
    herbivore = Organism(
        name = "Herbivore_Test", 
        species = "Herbivore",
        age = 5,
        energy = 100,
        position = Position(x=1, y=1),
        traits = HerbivoreTraits(
            detectionRadius = 5,
            speed = 1,
            energyCapacity = 250,
            birthEnergy = 80,
            slowDownAge = 30,
            reproductionAge = 20,
            matingCallRadius = 200,
            digestionTime = 8,
            generation = 1
        ),
        simulation = simulation
    )
    herbivore.simulation.organismList.append(herbivore)
    carnivore = Organism(
        name = "Carnivore_Test", 
        species = "Carnivore",
        age = 5,
        energy = 100,
        position = Position(x=9, y=9),
        traits = CarnivoreTraits(
            huntingRadius = 5,
            speed = 4,
            energyCapacity = 250,
            birthEnergy = 80,
            slowDownAge = 30,
            reproductionAge = 20,
            matingCallRadius = 200,
            digestionTime = 8,
            generation = 1
        ),
        simulation = simulation
    )
    carnivore.simulation.organismList.append(carnivore)
    simulation.run(ticks = 10)

if __name__ == "__main__":
    main()