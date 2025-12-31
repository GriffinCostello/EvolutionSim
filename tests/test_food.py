import simpy
import numpy as np
import random
import math
import pytest

from src.simulation import Simulation
from src.traits import *
from src.position import Position
from src.organism import Organism
from src.food import Food, FoodStage


#Tests if food is ages properly
def test_food_aging_and_stage_transition():
    simulation = Simulation(worldsize=4)
    food = Food(
        age = 0,
        position = Position(
            x = 1, 
            y = 1
        ), 
        traits = FoodTraits(
            generation = 1,
            stageConfiguration = {
                FoodStage.SEED: {"duration": 5, "nutrition": 100},
                FoodStage.RIPENING: {"duration": 5, "nutrition": 200},
                FoodStage.RIPE: {"duration": 5, "nutrition": 300},
                FoodStage.ROTTING: {"duration": 5, "nutrition": 150},
                FoodStage.ROTTEN: {"duration": 5, "nutrition": 50},
                }                   
        ),
        simulation = simulation
    )

    expectedStages = [
        (0, FoodStage.SEED),
        (5, FoodStage.RIPENING),
        (10, FoodStage.RIPE),
        (15, FoodStage.ROTTING),
        (20, FoodStage.ROTTEN)
    ]
    for tickCount, expectedStage in expectedStages:
        while food.age < tickCount:
            simulation.env.step()
        assert food.getStage() == expectedStage, f"At age {food.age}, expected stage {expectedStage} but got {food.getStage()}."


#tests if food is placed correctly after an organism poops
def test_food_placement_after_poop():
    simulation = Simulation(worldsize=4)
    food1 = Food(
        age = 10,
        position = Position(
            x = 1, 
            y = 1
        ), 
        traits = FoodTraits(
            generation = 1,
            stageConfiguration = {
                FoodStage.SEED: {"duration": 5, "nutrition": 100},
                FoodStage.RIPENING: {"duration": 5, "nutrition": 200},
                FoodStage.RIPE: {"duration": 5, "nutrition": 300},
                FoodStage.ROTTING: {"duration": 5, "nutrition": 150},
                FoodStage.ROTTEN: {"duration": 5, "nutrition": 50},
                }                   
        ),
        simulation = simulation
    )
    simulation.world[food1.position.x, food1.position.y] = food1

    herbivore = Organism(
        name = "Herbivore_Test", 
        species = "Herbivore",
        age = 5,
        energy = 100,
        position = Position(
            x=1, y=1
        ),
        traits = HerbivoreTraits(
            detectionRadius = 5,
            speed = 0,
            energyCapacity = 250,
            birthEnergy = 80,
            slowDownAge = 30,
            reproductionAge = 20,
            matingCallRadius = 200,
            digestionTime = 2,
            generation = 1
        ),
        simulation = simulation
    )
    herbivore.simulation.organismList.append(herbivore)

    simulation.run(ticks = 5)
    
    items = [x for x in simulation.world.flatten().tolist() if x is not None]
    for food in items:
        assert food.generation != 1, "New food from poop has incorrect generation."


