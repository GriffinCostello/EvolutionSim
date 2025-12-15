import simpy
import numpy as np
import random
import math

from simulation import Simulation
from traits import Traits
from position import Position
from organism import Organism



def main():
    sim = Simulation(worldsize=1000)

    genOneTraits = Traits(
        detectionRadius = 20,
        speed = 5,
        energy = 50,
        energyCapacity = 150,
        slowDownAge = 30,
        reproductionAge = 10,
        matingCallRadius = 200,
        generation = 1
    )

    for i in range(200):
        org = Organism(
            name = "Lion_Gen1_" + str(i), 
            species = "Lion", 
            age = random.randint(1, 10), 
            position = Position(
                x=np.random.randint(0, sim.worldSize),
                y=np.random.randint(0, sim.worldSize)
            ),
            traits = genOneTraits,
            sim = sim
        )
        org.sim.organismList.append(org)
    """
    for i in range(50):
        org = Organism(
            name = "Zebra_Gen1_" + str(i), 
            species = "Zebra", 
            age = random.randint(1, 10), 
            position = Position(
                x=np.random.randint(0, sim.worldSize),
                y=np.random.randint(0, sim.worldSize)
            ),
            traits = genOneTraits,
            sim = sim
        )
        org.sim.organismList.append(org)
    """

    sim.run(ticks = 500000)

if __name__ == "__main__":
    main()