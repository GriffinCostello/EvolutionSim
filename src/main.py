import simpy
import numpy as np
import random
import math

from simulation import Simulation
from traits import *
from position import Position
from organism import Organism



def main():
    simulation = Simulation(worldsize=1000)

    for i in range(100):
        org = Organism(
            name = "Herbivore_Gen1_" + str(i), 
            species = "Herbivore",
            age = random.randint(1, 10),
            energy = random.randint(40,60),
            position = Position(
                x=np.random.randint(0, simulation.worldSize),
                y=np.random.randint(0, simulation.worldSize)
            ),
            traits = HerbivoreTraits(
                detectionRadius = 30,
                speed = 8,
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
        org.simulation.organismList.append(org)

    simulation.run(ticks = 500000)

if __name__ == "__main__":
    main()