import simpy
import numpy as np
import random
import math

from .simulation import Simulation
from .traits import *
from .position import Position
from .organism import Organism



def main():
    simulation = Simulation(worldsize=1000)

    for i in range(110):
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
        org.simulation.traitLog[org.traits.generation].append(org.traits.speed)

    simulation.run(ticks = 500000)
    simulation.plotTraitEvolutionSpeed()

if __name__ == "__main__":
    main()