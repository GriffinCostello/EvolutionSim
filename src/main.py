import random

from .simulation import Simulation
from .traits import *
from .position import Position
from .organism import Organism



def main():
    simulation = Simulation(worldsize=1000)

    #Add initial herbivores
    for i in range(1000):
        simulation.createInitialHerbivores(i)

    #Add initial carnivores
    for i in range(100):
        simulation.createInitialCarnivores(i)

    simulation.run(ticks = 50000)
    simulation.statistics.plotTraitEvolution("speed")
    simulation.statistics.plotTraitEvolution("energyCapacity")
    simulation.statistics.plotTraitEvolution("reproductionAge")

if __name__ == "__main__":
    main()