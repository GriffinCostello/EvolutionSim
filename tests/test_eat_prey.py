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
        energy = 100,
        position = Position(x=9, y=9),
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
    simulation.run(ticks = 10)
    assert carnivore.energy > 100, "Carnivore did not gain energy after eating prey."
    assert herbivore not in simulation.organismList, "Herbivore was not removed from the simulation after being eaten."
    assert herbivore.age in simulation.lifeSpan, "Herbivore's age at death was not recorded in lifeSpan."
    assert carnivore in simulation.organismList, "Carnivore was incorrectly removed from the simulation."
    assert len(simulation.organismList) == 1, "There should be only one organism left in the simulation."