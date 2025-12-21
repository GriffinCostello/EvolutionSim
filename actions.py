import simpy
import numpy as np
import random
import math

from position import Position
from food import Food
from traits import *

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
        oppositeAdjacent = int(math.sqrt(self.org.traits.detectionRadius**2 / 2)) 
        xMin = max(self.org.position.x - oppositeAdjacent, 0)
        xMax = min(self.org.position.x + oppositeAdjacent + 1, self.org.simulation.worldSize)
        yMin = max(self.org.position.y - oppositeAdjacent, 0)
        yMax = min(self.org.position.y + oppositeAdjacent + 1, self.org.simulation.worldSize)

        # Slice region around the organism
        area = self.org.simulation.world[xMin:xMax, yMin:yMax]
        # Find actual coordinates of food
        foodPositions = np.argwhere(area != None) 
        if len(foodPositions) == 0:
            return None

        bestFood = None
        bestScore = 0

        for fx, fy in foodPositions:
            foodX = int(xMin + fx)
            foodY = int(yMin + fy)

            food = self.org.simulation.world[foodX, foodY]
            nutrition = food.getNutrition()
            distance = self.org.position.distanceTo(Position(foodX, foodY))

            # Formula that calculates best score based off nutrition and distance
            score = nutrition / (distance + 1)

            if score > bestScore:
                bestScore = score
                bestFood = (foodX, foodY)
            
        return bestFood

    
    def moveTowards(self, target):
        targetX, targetY = target
        speedRemaining = self.org.traits.speed
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


    def eatFood(self, bestFood):
        bestFoodX, bestFoodY = bestFood
        if self.org.simulation.world[bestFoodX, bestFoodY] is not None:
            nutritionalValue = self.org.simulation.world[bestFoodX, bestFoodY].getNutrition()
            foodTraits = self.org.simulation.world[bestFoodX, bestFoodY].traits
            self.org.simulation.world[bestFoodX, bestFoodY] = None  # Remove food from the world
            #print(f"{self.org.name} ate food at ({bestFoodX}, {bestFoodY})")
        else:
            print(f"{self.org.name} can't find food to eat at this position.")
            return

        self.org.energy = min(
            self.org.energy + nutritionalValue, 
            self.org.traits.energyCapacity
        )  # Gain energy

        yield self.org.simulation.env.timeout(self.org.traits.digestionTime)
        self.org.actions.poop(self.org, foodTraits)
        


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
                if distance <= self.org.traits.speed + otherOrganism.traits.speed and otherOrganism.energy > otherOrganism.traits.birthEnergy and self.org.energy > self.org.traits.birthEnergy:
                    self.org.simulation.mate(self.org, otherOrganism)


    def poop(self, org, foodTraits):
        stageConfigurationCopy = {}
        
        # Copy stage configuration 
        for stage, dictionary in foodTraits.stageConfiguration.items():
            # stage-specific variation ranges
            if stage == FoodStage.SEED:
                duration = random.randint(-1, 1)
                nutrition = random.randint(-1, 1)
            elif stage == FoodStage.RIPE:
                duration = random.randint(-3, 3)
                nutrition = random.randint(-5, 5)
            else:
                duration = random.randint(-2, 2)
                nutrition = random.randint(-2, 2)

            stageConfigurationCopy[stage] = {
                "duration": max(1, dictionary["duration"] + duration),
                "nutrition": max(0, dictionary["nutrition"] + nutrition),
            }

        org.simulation.world[org.position.x, org.position.y] = Food(
            age=0,
            position=Position(
                x=org.position.x,
                y=org.position.y
            ),
            traits=FoodTraits(
                generation=foodTraits.generation + 1,
                stageConfiguration=stageConfigurationCopy
            ),
            simulation=org.simulation
        )