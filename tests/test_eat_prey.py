import simpy
import numpy as np
import random
import math

from src.simulation import Simulation
from src.traits import *
from src.position import Position
from src.organism import Organism

def test_carnivore_eats_herbivore():
    simulation = Simulation(worldsize=10)
    herbivore = Organism(
        name = "Herbivore_Test", 
        species = "Herbivore",
        age = 5,
        energy = 100,
        position = Position(x=1, y=1),
        traits = HerbivoreTraits(
            detectionRadius = 5,
            speed = 1,
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
    herbivore.simulation.organismList.append(herbivore)
    carnivore = Organism(
        name = "Carnivore_Test", 
        species = "Carnivore",
        age = 5,
        energy = 90,
        position = Position(x=2, y=2),
        traits = CarnivoreTraits(
            huntingRadius = 5,
            speed = 4,
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
    carnivore.simulation.organismList.append(carnivore)
    simulation.run(ticks = 1)
    print(carnivore.position.asTuple())
    assert carnivore.energy > 100, "Carnivore did not gain energy after eating prey."
    assert herbivore not in simulation.organismList, "Herbivore was not removed from the simulation after being eaten."
    assert herbivore.age in simulation.statistics.lifeSpan, "Herbivore's age at death was not recorded in lifeSpan."
    assert carnivore in simulation.organismList, "Carnivore was incorrectly removed from the simulation."
    assert len(simulation.organismList) == 1, "There should be only one organism left in the simulation."


#Tests that a carnivore loses energy when no prey is available, and they don't eat eachother (YET)
def test_carnivore_no_prey():
    simulation = Simulation(worldsize=4)
    carnivore1 = Organism(
        name = "Carnivore_NoPrey", 
        species = "Carnivore1",
        age = 5,
        energy = 90,
        position = Position(x=1, y=1),
        traits = CarnivoreTraits(
            huntingRadius = 2,
            speed = 4,
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
    carnivore1.simulation.organismList.append(carnivore1)

    carnivore2 = Organism(
        name = "Carnivore_NoPrey", 
        species = "Carnivore1",
        age = 5,
        energy = 90,
        position = Position(x=3, y=3),
        traits = CarnivoreTraits(
            huntingRadius = 2,
            speed = 4,
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
    carnivore2.simulation.organismList.append(carnivore2)

    initial_energy = carnivore1.energy
    simulation.run(ticks = 5)
    assert carnivore1.energy < initial_energy, "Carnivore did not lose energy when no prey was available."
    assert carnivore2.energy < initial_energy, "Carnivore did not lose energy when no prey was available."
    assert carnivore1 in simulation.organismList, "Carnivore was incorrectly removed from the simulation."
    assert carnivore2 in simulation.organismList, "Carnivore was incorrectly removed from the simulation."
    assert len(simulation.organismList) == 2, "There should be two organisms left in the simulation."