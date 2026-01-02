import simpy
import numpy as np
import random
import math

from src.simulation import Simulation
from src.traits import *
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
    simulation.run(ticks = 1)

    assert food1 not in simulation.world.flatten(), "Best food source was incorrectly removed from the simulation."
    assert food2 in simulation.world.flatten(), "Non-chosen food source was incorrectly removed from the simulation."