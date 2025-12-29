import simpy
import numpy as np
import random
import math

from position import Position
from food import Food
from traits import *

class Actions:
    def __init__(self, organism: "Organism"):
        self.org = organism


    #Choose the next action for what to do
    def decideNextAction(self):
        if self.org.energy > self.org.traits.energyCapacity * 0.7:
            if(self.org.age >= self.org.traits.reproductionAge):
                return "Mate"

        # Choose scanning method depending on trait type
        target = None
        if isinstance(self.org.traits, HerbivoreTraits):
            target = self.scanForFood()
        elif isinstance(self.org.traits, CarnivoreTraits):
            target = self.scanForPrey()

        if target:
            return "LookForFood"
        else:
            return "Wander"


    #Looks for food nearby
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

        return self.findBestFood(foodPositions, xMin, xMax, yMin, yMax)


    # Looks for prey nearby for carnivores
    def scanForPrey(self):
        bestPrey = None
        bestScore = 0
        for other in self.org.simulation.organismList:
            if other is self.org:
                continue
            if other.species == self.org.species:
                continue

            distance = self.org.position.distanceTo(other.position)
            if distance > self.org.traits.huntingRadius:
                continue

            score = other.energy / (distance + 1)
            if score > bestScore:
                bestScore = score
                bestPrey = other

        return bestPrey
        

    #Finds the best food for Herbivores
    def findBestFood(self, foodPositions, xMin, xMax, yMin, yMax):
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


    #moves an organism towards a location
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


    #Eats food at a location
    def eatFood(self, bestFood):
        bestFoodX, bestFoodY = bestFood
        if self.org.simulation.world[bestFoodX, bestFoodY] is not None:
            nutritionalValue = self.org.simulation.world[bestFoodX, bestFoodY].getNutrition()
            foodTraits = self.org.simulation.world[bestFoodX, bestFoodY].traits
            self.org.simulation.world[bestFoodX, bestFoodY] = None  
        else:
            #print(f"{self.org.name} can't find food to eat at this position.")
            return

        self.org.energy = min(
            self.org.energy + nutritionalValue, 
            self.org.traits.energyCapacity
        )  # Gain energy

        yield self.org.simulation.env.timeout(self.org.traits.digestionTime)
        self.org.actions.poop(self.org, foodTraits)
        
    
    #Eats food at a location
    def eatPrey(self, prey):
        if prey in self.org.simulation.organismList:
            gainedEnergy = prey.energy
            prey.energy = -(1000000)  # Ensure prey dies, lets the live() method handle removal
        else:
            return

        self.org.energy = min(
            self.org.energy + gainedEnergy, 
            self.org.traits.energyCapacity
        )  # Gain energy
        print(f"{self.org.name} has eaten {prey.name} and gained {gainedEnergy} energy.")
        yield self.org.simulation.env.timeout(self.org.traits.digestionTime)
        


    #Looks for mates nearby and either moves towards them or mates with them
    def matingCall(self):
        for otherOrganism in self.org.simulation.organismList:
            if otherOrganism == self.org:
                continue
            if otherOrganism.age < otherOrganism.traits.reproductionAge:
                continue 
            if type(self.org.traits) is not type(otherOrganism.traits):
                return
            distance = self.org.position.distanceTo(otherOrganism.position)

            if distance <= self.org.traits.matingCallRadius:
                position = (otherOrganism.position.x, otherOrganism.position.y)
                self.org.actions.moveTowards(position)
                if distance <= self.org.traits.speed + otherOrganism.traits.speed and otherOrganism.energy > otherOrganism.traits.birthEnergy and self.org.energy > self.org.traits.birthEnergy:
                    self.org.simulation.mate(self.org, otherOrganism)


    #Organism poops out the foodtraits as a seed
    def poop(self, org, foodTraits):
        stageConfigurationCopy = {}

        # Copy stage configuration 
        for stage, dictionary in foodTraits.stageConfiguration.items():
            # stage-specific variation ranges
            if stage == FoodStage.SEED:
                stageConfigurationCopy[stage] = {
                    "duration": max(1, org.simulation.inherit(dictionary["duration"] , 1, 1)),
                    "nutrition": max(0, org.simulation.inherit(dictionary["nutrition"] , 1, 1)),
                }
            elif stage == FoodStage.RIPE:
                stageConfigurationCopy[stage] = {
                    "duration": max(1, org.simulation.inherit(dictionary["duration"] , 3, 1)),
                    "nutrition": max(0, org.simulation.inherit(dictionary["nutrition"] , 5, 1)),
                }
            else:
                stageConfigurationCopy[stage] = {
                    "duration": max(1, org.simulation.inherit(dictionary["duration"] , 2, 1)),
                    "nutrition": max(0, org.simulation.inherit(dictionary["nutrition"] , 2, 1)),
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