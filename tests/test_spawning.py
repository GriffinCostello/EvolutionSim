import simpy
import numpy as np
import random
import math

from src.simulation import Simulation
from src.traits import *
from src.position import Position
from src.organism import Organism
from src.food import Food, FoodStage

def test_organism_same_spawn():
    simulation = Simulation(worldsize=4) #4x4 world
    herbivore1 = Organism(
        name = "Herbivore_Test", 
        species = "Herbivore",
        age = 5,
        energy = 100,
        position = Position(x=0, y=0),
        traits = HerbivoreTraits(
            detectionRadius = 5,
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
    herbivore2 = Organism(
        name = "Herbivore_Test2",
        species = "Herbivore",
        age = 5,
        energy = 100,
        position = Position(x=0, y=0),
        traits = HerbivoreTraits(
            detectionRadius = 5,
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
    assert herbivore1.position.asTuple() == herbivore2.position.asTuple(), "Organisms spawned at different position."
    simulation.run(ticks = 1)
    assert herbivore1.position.asTuple() == herbivore2.position.asTuple(), "Organisms moved apart after spawning at the same position, they should stay in the same position due to 0 speed."

def test_food_same_spawn():
    xTest = 1
    yTest = 1
    simulation = Simulation(worldsize=4) #4x4 world
    food1 = Food(
        age = random.randint(20, 25),
        position = Position(
            x = xTest, 
            y = yTest
        ), 
        traits = FoodTraits(
            generation = 1,
            stageConfiguration = {
                FoodStage.SEED: {"duration": random.randint(7, 10), "nutrition": 500},
                FoodStage.RIPENING: {"duration": random.randint(8, 15), "nutrition": 500},
                FoodStage.RIPE: {"duration": random.randint(18, 25), "nutrition": 500},
                FoodStage.ROTTING: {"duration": random.randint(8, 15), "nutrition": 500},
                FoodStage.ROTTEN: {"duration": random.randint(7, 10), "nutrition": 500},
                }                   
        ),
        simulation = simulation
    )
    simulation.world[food1.position.x, food1.position.y] = food1
    food2 = Food(
        age = random.randint(20, 25),
        position = Position(
            x = xTest, 
            y = yTest
        ), 
        traits = FoodTraits(
            generation = 1,
            stageConfiguration = {
                FoodStage.SEED: {"duration": random.randint(7, 10), "nutrition": 500},
                FoodStage.RIPENING: {"duration": random.randint(8, 15), "nutrition": 500},
                FoodStage.RIPE: {"duration": random.randint(18, 25), "nutrition": 500},
                FoodStage.ROTTING: {"duration": random.randint(8, 15), "nutrition": 500},
                FoodStage.ROTTEN: {"duration": random.randint(7, 10), "nutrition": 500},
                }                   
        ),
        simulation = simulation
    )
    simulation.world[xTest, yTest] = food2
    assert simulation.world[xTest, yTest] == food2, "Second food did not overwrite the first food at the same position."
    assert simulation.world[xTest, yTest] != food1, "First food still exists at the position after second food spawned there."
    simulation.run(ticks = 1)
    assert simulation.world[xTest, yTest] == food2, "Food position changed after simulation run, it should remain the same."
    assert simulation.world[xTest, yTest] != food1, "First food reappeared at the position after simulation run."