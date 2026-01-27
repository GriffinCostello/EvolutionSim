import simpy
import numpy as np
import random
import math
import pytest

from src.simulation import Simulation
from src.traits import *
from src.genetics import *
from src.position import Position
from src.organism import Organism
from src.food import Food, FoodStage


#tests if organisms spawn correctly at the same position
def test_organism_same_spawn():
    simulation = Simulation(worldsize=4) #4x4 world
    herbivore1 = Organism(
        name = "Herbivore_Test", 
        species = "Herbivore",
        age = 5,
        energy = 100,
        position = Position(x=0, y=0),
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

    herbivore2 = Organism(
        name = "Herbivore_Test2",
        species = "Herbivore",
        age = 5,
        energy = 100,
        position = Position(x=0, y=0),
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

    assert herbivore1.position.asTuple() == herbivore2.position.asTuple(), "Organisms spawned at different position."
    assert len(simulation.organismList) == 2, "Herbivore1 or Herbivore2 not correctly added to simulation."
    simulation.run(ticks = 1)
    assert herbivore1.position.asTuple() == herbivore2.position.asTuple(), "Organisms moved apart after spawning at the same position, they should stay in the same position due to 0 speed."
    assert len(simulation.organismList) == 2, "Herbivore1 or Herbivore2 not correctly added to simulation."


#test if food spawns correctly at the same position (overwriting previous food)
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
    simulation.world.place(food1, food1.position)

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
    simulation.world.place(food2, food2.position)

    assert simulation.world.getObjectAt(Position(xTest, yTest)) == food2, "Second food did not overwrite the first food at the same position."
    assert simulation.world.getObjectAt(Position(xTest, yTest))  != food1, "First food still exists at the position after second food spawned there."
    simulation.run(ticks = 1)
    assert simulation.world.getObjectAt(Position(xTest, yTest))  == food2, "Food position changed after simulation run, it should remain the same."
    assert simulation.world.getObjectAt(Position(xTest, yTest))  != food1, "First food reappeared at the position after simulation run."


#test organisms and food spawning out of bounds
def test_organism_out_of_bounds():
    simulation = Simulation(worldsize=4) #4x4 world

    with pytest.raises(ValueError):
        herbivore1 = Organism(
            name = "Herbivore_Test", 
            species = "Herbivore",
            age = 5,
            energy = 100,
            position = Position(x=4, y=4), #Out of bounds
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
    assert len(simulation.organismList) == 0, "Organism out of bounds was added to the simulation."

    with pytest.raises(ValueError):
        herbivore2 = Organism(
            name = "Herbivore_Test", 
            species = "Herbivore",
            age = 5,
            energy = 100,
            position = Position(x=-1, y=-1), #Out of bounds
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
    assert len(simulation.organismList) == 0, "Organism out of bounds was added to the simulation."


#tests food spawning out of bounds
def test_food_out_of_bounds():
    simulation = Simulation(worldsize=4) #4x4 world

    with pytest.raises(ValueError):
        food1 = Food(
            age = random.randint(20, 25),
            position = Position(
                x = 4,  #Out of bounds
                y = 4
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
        simulation.world.place(food1, food1.position)

    sumList = simulation.world.flatten()
    count = sum(x is not None for x in sumList)
    assert count == 0, "Food out of bounds was added to the simulation."

    with pytest.raises(ValueError):
        food2 = Food(
            age = random.randint(20, 25),
            position = Position(
                x = -1,  #Out of bounds
                y = -1
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
        simulation.world.place(food2, food2.position)

    sumList = simulation.world.flatten()
    count = sum(x is not None for x in sumList)
    assert count == 0, "Food out of bounds was added to the simulation."


#Tests carnivore reproductive behavior
def test_carnivore_reproduction():
    simulation = Simulation(worldsize=4)
    carnivore1 = Organism(
        name = "Carnivore_NoPrey", 
        species = "Carnivore1",
        age = 25,
        energy = 200,
        position = Position(x=3, y=3),
        genetics = CarnivoreGenetics(
            huntingRadius = 2,
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
    carnivore1.simulation.organismList.append(carnivore1)
    carnivore1.simulation.carnivoreList.append(carnivore1)

    carnivore2 = Organism(
        name = "Carnivore_NoPrey", 
        species = "Carnivore1",
        age = 25,
        energy = 200,
        position = Position(x=3, y=3),
        genetics = CarnivoreGenetics(
            huntingRadius = 2,
            speed = 1,
            energyCapacity = 300,
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
    carnivore2.simulation.carnivoreList.append(carnivore2)

    simulation.run(ticks = 1)
    assert carnivore1 in simulation.organismList, "Carnivore was incorrectly removed from the simulation."
    assert carnivore2 in simulation.organismList, "Carnivore was incorrectly removed from the simulation."
    assert len(simulation.organismList) == 3, "No offspring was produced after carnivores mated or too many organisms present."
    for x in simulation.organismList:
        if x not in [carnivore1, carnivore2]:
            assert isinstance(x.genetics, CarnivoreGenetics), "Offspring does not have Carnivore Genetics."
            assert x.traits.generation == 2, "Offspring generation is not correct."
            assert x.traits.energyCapacity <= (carnivore1.traits.energyCapacity + carnivore2.traits.energyCapacity)//2 + 10, "Offspring energy capacity is too high."
            assert x.traits.energyCapacity >= (carnivore1.traits.energyCapacity + carnivore2.traits.energyCapacity)//2 - 10, "Offspring energy capacity is too low."


#Tests herbivore reproductive behavior
def test_herbivore_reproduction():
    simulation = Simulation(worldsize=4)
    herbivore1 = Organism(
        name = "Herbivore_NoPrey", 
        species = "Herbivore1",
        age = 25,
        energy = 200,
        position = Position(x=2, y=2),
        genetics = HerbivoreGenetics(
            foodDetectionRadius = 5,
            predatorDetectionRadius = 2,
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
    herbivore1.simulation.organismList.append(herbivore1)
    herbivore1.simulation.herbivoreList.append(herbivore1)

    herbivore2 = Organism(
        name = "Herbivore_NoPrey", 
        species = "Herbivore1",
        age = 25,
        energy = 200,
        position = Position(x=2, y=2),
        genetics = HerbivoreGenetics(
            foodDetectionRadius = 5,
            predatorDetectionRadius = 2,
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
    herbivore2.simulation.organismList.append(herbivore2)
    herbivore2.simulation.herbivoreList.append(herbivore2)

    simulation.run(ticks = 2)
    assert herbivore1 in simulation.organismList, "Herbivore was incorrectly removed from the simulation."
    assert herbivore2 in simulation.organismList, "Herbivore was incorrectly removed from the simulation."
    assert len(simulation.organismList) == 3, "No offspring was produced after herbivores mated or too many organisms present."
    for x in simulation.organismList:
        if x not in [herbivore1, herbivore2]:
            assert isinstance(x.genetics, HerbivoreGenetics), "Offspring does not have Herbivore Genetics."
            assert x.traits.generation == 2, "Offspring generation is not correct."
            assert x.traits.energyCapacity <= (herbivore1.traits.energyCapacity + herbivore2.traits.energyCapacity)//2 + 10, "Offspring energy capacity is too high."
            assert x.traits.energyCapacity >= (herbivore1.traits.energyCapacity + herbivore2.traits.energyCapacity)//2 - 10, "Offspring energy capacity is too low."