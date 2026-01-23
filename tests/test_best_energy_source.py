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

def test_best_food():
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
    herbivore.simulation.organismList.append(herbivore)
    herbivore.simulation.herbivoreList.append(herbivore)
    
    food1 = Food(
        age = 20,
        position = Position(
            x = 1, 
            y = 2
        ), 
        traits = FoodTraits(
            generation = 1,
            stageConfiguration = {
                FoodStage.SEED: {"duration": 10, "nutrition": 500},
                FoodStage.RIPENING: {"duration": 20, "nutrition": 500},
                FoodStage.RIPE: {"duration": 10, "nutrition": 500},
                FoodStage.ROTTING: {"duration": 10, "nutrition": 500},
                FoodStage.ROTTEN: {"duration": 10, "nutrition": 500},
                }                   
        ),
        simulation = simulation
    )
    food1.simulation.world.place(food1, food1.position)

    food2 = Food(
        age = 20,
        position = Position(
            x = 2, 
            y = 1
        ), 
        traits = FoodTraits(
            generation = 1,
            stageConfiguration = {
                FoodStage.SEED: {"duration": 10, "nutrition": 50},
                FoodStage.RIPENING: {"duration": 20, "nutrition": 50},
                FoodStage.RIPE: {"duration": 10, "nutrition": 50},
                FoodStage.ROTTING: {"duration": 10, "nutrition": 50},
                FoodStage.ROTTEN: {"duration": 10, "nutrition": 50},
                }                   
        ),
        simulation = simulation
    )
    food2.simulation.world.place(food2, food2.position)

    food3 = Food(
        age = 20,
        position = Position(
            x = 1, 
            y = 0
        ), 
        traits = FoodTraits(
            generation = 1,
            stageConfiguration = {
                FoodStage.SEED: {"duration": 10, "nutrition": 5},
                FoodStage.RIPENING: {"duration": 20, "nutrition": 5},
                FoodStage.RIPE: {"duration": 10, "nutrition": 5},
                FoodStage.ROTTING: {"duration": 10, "nutrition": 5},
                FoodStage.ROTTEN: {"duration": 10, "nutrition": 5},
                }                   
        ),
        simulation = simulation
    )
    food3.simulation.world.place(food3, food3.position)


    simulation.run(ticks = 1)

    assert food1 not in simulation.world.flatten(), "Best food source was incorrectly removed from the simulation."
    assert food2 in simulation.world.flatten(), "Non-chosen food source was incorrectly removed from the simulation."
    assert food3 in simulation.world.flatten(), "Non-chosen food source was incorrectly removed from the simulation."


def test_best_Prey():
    simulation = Simulation(worldsize=3)
    carnivore = Organism(
        name = "Carnivore_NoPrey", 
        species = "Carnivore1",
        age = 25,
        energy = 50,
        position = Position(
            x=0, 
            y=0
        ),
        genetics = CarnivoreGenetics(
            huntingRadius = 4,
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
    carnivore.simulation.carnivoreList.append(carnivore)

    herbivore1 = Organism(
        name = "Herbivore_Test", 
        species = "Herbivore",
        age = 5,
        energy = 1000,
        position = Position(
            x=2, 
            y=1
        ),
        genetics = HerbivoreGenetics(
            foodDetectionRadius = 5,
            predatorDetectionRadius = 2,
            speed = 0,
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
    herbivore1.simulation.organismList.append(herbivore1)
    herbivore1.simulation.herbivoreList.append(herbivore1)

    herbivore2 = Organism(
        name = "Herbivore_Test", 
        species = "Herbivore",
        age = 5,
        energy = 500,
        position = Position(
            x=1, 
            y=2
        ),
        genetics = HerbivoreGenetics(
            foodDetectionRadius = 5,
            predatorDetectionRadius = 2,
            speed = 0,
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
    herbivore2.simulation.organismList.append(herbivore2)
    herbivore2.simulation.herbivoreList.append(herbivore2)

    herbivore3 = Organism(
        name = "Herbivore_Test", 
        species = "Herbivore",
        age = 5,
        energy = 500,
        position = Position(
            x=0, 
            y=1
        ),
        genetics = HerbivoreGenetics(
            foodDetectionRadius = 5,
            predatorDetectionRadius = 2,
            speed = 0,
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
    herbivore3.simulation.organismList.append(herbivore3)
    herbivore3.simulation.herbivoreList.append(herbivore3)
    
    simulation.run(ticks = 1)

    assert herbivore1 not in simulation.organismList, "Carnivore did not eat the best prey available."
    assert herbivore2 in simulation.organismList, "Carnivore incorrectly ate the worse prey."
    assert herbivore3 in simulation.organismList, "Carnivore incorrectly ate the worse prey."