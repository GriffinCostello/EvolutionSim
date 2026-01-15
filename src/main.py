import time

from .simulation import Simulation
from .traits import *
from .position import Position
from .organism import Organism



def main():
    start = time.time()
    simulation = Simulation(worldsize=1000, startTime = start)

    #Add initial herbivores
    for i in range(1000):
        simulation.createInitialHerbivores(i)

    #Add initial carnivores
    for i in range(100):
        simulation.createInitialCarnivores(i)

    simulation.run(ticks = 50000)
    # Print average lifespan summary once at end of run (covers timeout or all-dead)
    totalAverageLifeSpan = sum(simulation.statistics.lifeSpan) / len(simulation.statistics.lifeSpan)
    herbivoreAverageLifeSpan = sum(simulation.statistics.lifeSpanBySpecies.get("Herbivore", [1])) / len(simulation.statistics.lifeSpanBySpecies.get("Herbivore", [1]))
    carnivoreAverageLifeSpan = sum(simulation.statistics.lifeSpanBySpecies.get("Carnivore", [1])) / len(simulation.statistics.lifeSpanBySpecies.get("Carnivore", [1]))
    print(f"\nSimulation finished. Overall avg lifespan: {totalAverageLifeSpan:.4f}; Herbivore avg: {herbivoreAverageLifeSpan:.4f}; Carnivore avg: {carnivoreAverageLifeSpan:.4f}")

    simulation.statistics.plotTraitEvolution("speed")
    simulation.statistics.plotTraitEvolution("energyCapacity")
    simulation.statistics.plotTraitEvolution("reproductionAge")
    simulation.statistics.plotTraitEvolution("foodDetectionRadius")
    simulation.statistics.plotTraitEvolution("predatorDetectionRadius")

if __name__ == "__main__":
    main()