from src.world import World
from src.simulation import Simulation
from src.position import Position
from src.organism import Organism
from src.traits import HerbivoreTraits
from src.genetics import HerbivoreGenetics
import pytest

def test_world_size_zero():
    simulation = Simulation(worldsize=0)
    simulation.run(ticks=10)
    
    with pytest.raises(ValueError):
        herbivore = Organism(
            name = "Herbivore_Test", 
            species = "Herbivore",
            age = 5,
            energy = 100,
            position = Position(x=0, y=0),
            genetics = HerbivoreGenetics(
                foodDetectionRadius = 5,
                predatorDetectionRadius = 2,
                speed = 5,
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
        simulation.organismList.append(herbivore)

    assert simulation.world.worldSize == 0, "World size should be zero."