import simpy
import numpy as np
import random
import math

from src.simulation import Simulation
from src.traits import *
from src.position import Position
from src.organism import Organism
from src.food import Food, FoodStage

def test_carnivore_eats_herbivore():
    simulation = Simulation(worldsize=4)
    herbivore = Organism(
        name = "Herbivore_Test", 
        species = "Herbivore",
        age = 5,
        energy = 100,
        position = Position(x=1, y=1),
        traits = HerbivoreTraits(
            detectionRadius = 5,
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
    herbivore.simulation.organismList.append(herbivore)
    food = Food(
        age = random.randint(20, 25),
        position = Position(
            x = 2, 
            y = 2
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
    herbivore.simulation.world[food.position.x, food.position.y] = food
    simulation.run(ticks = 5)
    assert herbivore.energy > 100, "Herbivore did not gain energy after eating food."
    assert food not in simulation.world, "Food was not removed from the simulation after being eaten."
    assert simulation.world[food.position.x, food.position.y] is None, "Food position in the world was not cleared after being eaten."