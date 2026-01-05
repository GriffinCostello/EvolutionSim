import numpy as np

from .position import Position

class World:
    def __init__(self, worldsize):
        self.worldSize = worldsize
        self.grid = np.empty((self.worldSize, self.worldSize), dtype=object)
        self.grid.fill(None)


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