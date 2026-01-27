import numpy as np
import random

from .food import Food
from .traits import *
from .position import Position

class World:
    def __init__(self, worldsize, simulation: "Simulation"):
        self.worldSize = worldsize
        self.grid = np.empty((self.worldSize, self.worldSize), dtype=object)
        self.grid.fill(None)
        self.simulation = simulation

    def validPosition(self, position: Position):
        if not (0 <= position.x < self.worldSize and 0 <= position.y < self.worldSize):
            raise ValueError("Position out of bounds of the simulation world.")


    def place(self, obj, position: Position):
        self.validPosition(position)
        self.grid[position.x, position.y] = obj


    def remove(self, position: Position):
        self.validPosition(position)
        self.grid[position.x, position.y] = None


    def getObjectAt(self, position: Position):
        self.validPosition(position)
        return self.grid[position.x, position.y]


    def objectsInRegion(self, xMin, xMax, yMin, yMax):
        for x in range(xMin, xMax):
            for y in range(yMin, yMax):
                obj = self.grid[x, y]
                if obj is not None:
                    yield obj


    def flatten(self):
        for x in range(self.worldSize):
            for y in range(self.worldSize):
                obj = self.grid[x, y]
                if obj is not None:
                    yield obj


    #places food on the map
    def placeInitialFood(self, numFood):
        for i in range(0,numFood):
            x = random.randint(0, self.worldSize -1)
            y = random.randint(0, self.worldSize -1)
            food = Food(
                age = random.randint(0,50),
                position = Position(
                    x = x, 
                    y = y
                ), 
                traits = FoodTraits(
                    generation = 1,
                    stageConfiguration = {
                        FoodStage.SEED: {"duration": random.randint(7, 10), "nutrition": random.randint(50, 80)},
                        FoodStage.RIPENING: {"duration": random.randint(8, 15), "nutrition": random.randint(130, 150)},
                        FoodStage.RIPE: {"duration": random.randint(18, 25), "nutrition": random.randint(250, 300)},
                        FoodStage.ROTTING: {"duration": random.randint(8, 15), "nutrition": random.randint(200, 250)},
                        FoodStage.ROTTEN: {"duration": random.randint(7, 10), "nutrition": 0},
                    }                   
                ),
                #All food created in the world gets a reference to the simulation
                simulation = self.simulation
            )
            self.place(food, food.position)
