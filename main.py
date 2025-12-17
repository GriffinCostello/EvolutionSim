import simpy
import numpy as np
import random
import math

from simulation import Simulation
from traits import *
from position import Position
from organism import Organism



def main():
    sim = Simulation(worldsize=1000)

    for i in range(200):
        org = Organism(
            name = "Lion_Gen1_" + str(i), 
            species = "Lion",
            age = random.randint(1, 10),
            energy = random.randint(40,60),
            position = Position(
                x=np.random.randint(0, sim.worldSize),
                y=np.random.randint(0, sim.worldSize)
            ),
            traits = OrganismTraits(
                detectionRadius = 20,
                speed = 5,
                energyCapacity = 150,
                slowDownAge = 30,
                reproductionAge = 10,
                matingCallRadius = 200,
                generation = 1
            ),
            simulation = sim
        )
        org.simulation.organismList.append(org)

    numFood = (sim.worldSize * sim.worldSize) // 800
    sim.placeFood(
        numFood = numFood
    )

    sim.run(ticks = 500000)

if __name__ == "__main__":
    main()