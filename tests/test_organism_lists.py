import simpy
import numpy as np
import random
import math

from src.simulation import Simulation
from src.traits import *
from src.genetics import *
from src.position import Position
from src.organism import Organism
from src.food import Food, FoodStage

def test_herbivore_added_and_removed():
    simulation = Simulation(worldsize=3)
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

    assert herbivore in herbivore.simulation.organismList, "Herbivore was not added to organism list"
    assert herbivore in herbivore.simulation.herbivoreList, "Herbivore was not added to herbivore list"
    simulation.run(200)
    assert herbivore not in herbivore.simulation.organismList, "Herbivore was not removed from organism list"
    assert herbivore not in herbivore.simulation.herbivoreList, "Herbivore was not removed from herbivore list"


def test_carnivore_added_and_removed():
    simulation = Simulation(worldsize=3)
    carnivore = Organism(
        name = "Carnivore_Test", 
        species = "Carnivore",
        age = 5,
        energy = 100,
        position = Position(
            x=0, y=0
        ),
        genetics = CarnivoreGenetics(
            huntingRadius= 4,
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

    assert carnivore in carnivore.simulation.organismList, "carnivore was not added to organism list"
    assert carnivore in carnivore.simulation.carnivoreList, "carnivore was not added to carnivore list"
    simulation.run(200)
    assert carnivore not in carnivore.simulation.organismList, "carnivore was not removed from organism list"
    assert carnivore not in carnivore.simulation.carnivoreList, "carnivore was not removed from carnivore list"