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


#tests if herbivore eats food correctly
def test_herbivore_eats_food():
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

    simulation.run(ticks = 5)
    assert herbivore.energy > 100, "Herbivore did not gain energy after eating food."
    assert food not in simulation.world.flatten(), "Food was not removed from the simulation after being eaten."
    assert simulation.world.getObjectAt(Position(food.position.x, food.position.y)) is None, "Food position in the world was not cleared after being eaten."


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
    food = Food(
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
    
    items = simulation.world.flatten()
    for food in items:
        assert food.generation != 1, "New food from poop has incorrect generation."


