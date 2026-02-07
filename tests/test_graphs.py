
from src.simulation import Simulation
from src.traits import *
from src.genetics import *
from src.position import Position
from src.organism import Organism

def test_printing_herbivores():
    simulation = Simulation(worldsize=3)
    for i in range(0, 100):
        herbivore = Organism(
            name = "Herbivore_Test", 
            species = "Herbivore",
            age = 5,
            energy = 100,
            position = Position(
                x=0, y=0
            ),
            genetics = HerbivoreGenetics(
                foodDetectionRadius = 5,
                predatorDetectionRadius = 2,
                speed = i,
                energyCapacity = 250,
                birthEnergy = 80,
                slowDownAge = 30,
                reproductionAge = 20,
                matingCallRadius = 200,
                digestionTime = 8,
                generation = i
            ),
            simulation = simulation
        )
        herbivore.simulation.organismList.append(herbivore)
        herbivore.simulation.herbivoreList.append(herbivore)
        for geneticName, value in vars(herbivore.genetics).items():
                if geneticName != "generation":
                    simulation.statistics.logGeneticsHerbivore(geneticName, herbivore.genetics.generation, value)
    simulation.statistics.plotGeneticsEvolution("speed", "Herbivore")
    stats = simulation.statistics
    assert "speed" in stats.traitLogHerbivore
    assert len(stats.traitLogHerbivore["speed"]) == 100