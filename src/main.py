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


    #Add initial herbivores
    for i in range(1000):
        org = Organism(
            name = "Herbivore_Gen1_" + str(i), 
            species = "Herbivore",
            age = random.randint(1, 20),
            energy = random.randint(150,200),
            position = Position(
                x=np.random.randint(0, simulation.worldSize),
                y=np.random.randint(0, simulation.worldSize)
            ),
            traits = HerbivoreTraits(
                detectionRadius = 30,
                speed = 6,
                energyCapacity = 500,
                birthEnergy = 80,
                slowDownAge = 60,
                reproductionAge = 20,
                matingCallRadius = 200,
                digestionTime = 5,
                generation = 1
            ),
            simulation = simulation
        )
        org.simulation.organismList.append(org)
        for traitName, value in vars(org.traits).items():
            if traitName != "generation":
                simulation.traitLog[traitName][org.traits.generation].append(value)

    #Add initial carnivores
    for i in range(100):
        org = Organism(
            name = "Carnivore_Gen1_" + str(i), 
            species = "Carnivore",
            age = random.randint(1, 20),
            energy = random.randint(150,200),
            position = Position(
                x=np.random.randint(0, simulation.worldSize),
                y=np.random.randint(0, simulation.worldSize)
            ),
            traits = CarnivoreTraits(
                huntingRadius = 30,
                speed = 8,
                energyCapacity = 500,
                birthEnergy = 80,
                slowDownAge = 60,
                reproductionAge = 20,
                matingCallRadius = 200,
                digestionTime = 5,
                generation = 1
            ),
            simulation = simulation
        )
        org.simulation.organismList.append(org)

    simulation.run(ticks = 50000)
    simulation.plotTraitEvolution("speed")
    simulation.plotTraitEvolution("energyCapacity")
    simulation.plotTraitEvolution("reproductionAge")

if __name__ == "__main__":
    main()