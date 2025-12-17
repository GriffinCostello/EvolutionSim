import simpy
import numpy as np
import random
import math

from position import Position
from food import Food

class Actions:
    def __init__(self, organism: Orgnanism):
        self.org = organism


    def decideNextAction(self):
        if self.org.energy > self.org.traits.energyCapacity * 0.7:
            if(self.org.age >= self.org.traits.reproductionAge):
                return "Mate"

        closestFood = self.org.actions.scanForFood()
        if closestFood:
            return "LookForFood"
        else:
            return "Wander"


    def scanForFood(self):
        xMin = max(self.org.position.x - self.org.traits.detectionRadius, 0)
        xMax = min(self.org.position.x + self.org.traits.detectionRadius + 1, self.org.simulation.worldSize)
        yMin = max(self.org.position.y - self.org.traits.detectionRadius, 0)
        yMax = min(self.org.position.y + self.org.traits.detectionRadius + 1, self.org.simulation.worldSize)

        # Slice region around the organism
        area = self.org.simulation.world[xMin:xMax, yMin:yMax]
        # Find actual coordinates of food
        foodPositions = np.argwhere(area != None) 
        if len(foodPositions) == 0:
            return None  # No food found

        foodGlobal = [Position(int(xMin + foodX), int(yMin + foodY)) for foodX, foodY in foodPositions]
        closest = min(foodGlobal, key=lambda p: p.distanceTo(self.org.position))
        return closest.asTuple()

    
    def moveTowards(self, target):
        targetX, targetY = target
        if self.org.position.x < targetX:
            if(self.org.position.x + self.org.traits.speed > targetX): #if this step would overshoot
                self.org.position.x = targetX               #then just go to target
            else:
                self.org.position.x += self.org.traits.speed

        elif self.org.position.x > targetX:
            if(self.org.position.x - self.org.traits.speed < targetX):
                self.org.position.x = targetX
            else:
                self.org.position.x -= self.org.traits.speed

        if self.org.position.y < targetY:
            if(self.org.position.y + self.org.traits.speed > targetY):
                self.org.position.y = targetY
            else:
                self.org.position.y += self.org.traits.speed

        elif self.org.position.y > targetY:
            if(self.org.position.y - self.org.traits.speed < targetY):
                self.org.position.y = targetY
            else:
                self.org.position.y -= self.org.traits.speed

        self.org.energy = max(self.org.energy - self.org.traits.energyConsumption, 0)


    def eatFood(self, closestFood):
        closestFoodX, closestFoodY = closestFood
        NutritionValue = self.org.simulation.world[closestFoodX, closestFoodY].traits.nutritionValue
        if self.org.simulation.world[closestFoodX, closestFoodY] is not None:
            self.org.simulation.world[closestFoodX, closestFoodY] = None  # Remove food from the world
            print(f"{self.org.name} ate food at ({closestFoodX}, {closestFoodY})")
        else:
            print(f"{self.org.name} can't find food to eat at this position.")
            return

        self.org.energy = min(self.org.energy + NutritionValue, self.org.traits.energyCapacity)  # Gain energy


    def matingCall(self):

        for otherOrganism in self.org.simulation.organismList:
            if otherOrganism == self.org:
                continue
            if otherOrganism.age < otherOrganism.traits.reproductionAge:
                continue 
            if otherOrganism.species is not self.org.species:
                continue
            distance = self.org.position.distanceTo(otherOrganism.position)

            if distance <= self.org.traits.matingCallRadius:
                position = (otherOrganism.position.x, otherOrganism.position.y)
                self.org.actions.moveTowards(position)
                if distance <= self.org.traits.speed + otherOrganism.traits.speed and otherOrganism.energy > 50 and self.org.energy > 50:
                    self.org.simulation.mate(self.org, otherOrganism)