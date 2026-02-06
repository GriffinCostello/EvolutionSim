import time

from .simulation import Simulation
from .traits import *
from .position import Position
from .organism import Organism



def main():
    simulation = Simulation(worldsize=1000)

    #Add initial herbivores
    for i in range(1300):
        simulation.createInitialHerbivores(i)

    #Add initial carnivores
    for i in range(100):
        simulation.createInitialCarnivores(i)

    simulation.printTime()
    simulation.run(ticks = 50000)
    
    # Print average lifespan summary once at end of run (covers timeout or all-dead)
    totalAverageLifeSpan = sum(simulation.statistics.lifeSpan) / len(simulation.statistics.lifeSpan)
    herbivoreAverageLifeSpan = sum(simulation.statistics.lifeSpanBySpecies.get("Herbivore", [1])) / len(simulation.statistics.lifeSpanBySpecies.get("Herbivore", [1]))
    carnivoreAverageLifeSpan = sum(simulation.statistics.lifeSpanBySpecies.get("Carnivore", [1])) / len(simulation.statistics.lifeSpanBySpecies.get("Carnivore", [1]))
    print(f"\nSimulation finished. Overall avg lifespan: {totalAverageLifeSpan:.4f}; Herbivore avg: {herbivoreAverageLifeSpan:.4f}; Carnivore avg: {carnivoreAverageLifeSpan:.4f}")

    simulation.statistics.plotGeneticsEvolution("speed", "Herbivore")
    simulation.statistics.plotGeneticsEvolution("speed", "Carnivore")
    simulation.statistics.plotGeneticsEvolution("energyCapacity", "Herbivore")
    simulation.statistics.plotGeneticsEvolution("reproductionAge", "Herbivore")
    simulation.statistics.plotGeneticsEvolution("foodDetectionRadius", "Herbivore")
    simulation.statistics.plotGeneticsEvolution("predatorDetectionRadius", "Herbivore")

if __name__ == "__main__":
    main()