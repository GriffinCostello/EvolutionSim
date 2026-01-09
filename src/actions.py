import math

from .position import Position
from .food import Food
from .traits import *

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
        area = self.org.simulation.world.objectsInRegion(xMin, xMax, yMin, yMax)
        # Find actual coordinates of food
        foods = []
        for obj in area:
            foods.append(obj)
        
        bestFood = self.findBestFood(foods, xMin, xMax, yMin, yMax)
        if bestFood is None:
            return None

        return bestFood.position.asTuple()


    #Finds the best food for Herbivores
    def findBestFood(self, foods, xMin, xMax, yMin, yMax):
        bestFood = None
        bestScore = 0

        for food in foods:
            nutrition = food.getNutrition()
            distance = self.org.position.distanceTo(food.position)

            score = nutrition / (distance + 1)

            if score > bestScore:
                bestScore = score
                bestFood = food

        return bestFood


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
        bestFoodX , bestFoodY = bestFood
        foodToBeEaten = self.org.simulation.world.getObjectAt(Position(bestFoodX, bestFoodY))
        if foodToBeEaten is not None:
            nutritionalValue = foodToBeEaten.getNutrition()
            foodTraits = foodToBeEaten.traits
            foodToBeEaten.simulation.world.remove(foodToBeEaten.position)
        else:
            #print(f"{self.org.name} can't find food to eat at this position.")
            return

        self.org.energy = min(
            self.org.energy + nutritionalValue, 
            self.org.traits.energyCapacity
        )  # Gain energy

        self.org.simulation.env.process(self.digestAndPoop(foodTraits))


    #SimPy process for digestion and pooping seeds
    def digestAndPoop(self, foodTraits):
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
        


    #Looks for mates nearby and either moves towards them or mates with them
    def matingCall(self):
        org = self.org
        matingRadiusSquared = org.traits.matingCallRadius * org.traits.matingCallRadius

        for otherOrganism in org.simulation.organismList:
            if otherOrganism is org:
                continue
            if otherOrganism.age < otherOrganism.traits.reproductionAge:
                continue
            if type(org.traits) is not type(otherOrganism.traits):
                continue

            distanceToSquared = org.position.distanceSquaredTo(otherOrganism.position)

            if distanceToSquared <= matingRadiusSquared:
                position = (otherOrganism.position.x, otherOrganism.position.y)
                org.actions.moveTowards(position)
                speedThresholdSquared = (org.traits.speed + otherOrganism.traits.speed) * (org.traits.speed + otherOrganism.traits.speed)
                if distanceToSquared <= speedThresholdSquared and otherOrganism.energy > otherOrganism.traits.birthEnergy and org.energy > org.traits.birthEnergy:
                    org.reproduction.mate(otherOrganism)


    #Organism poops out the foodtraits as a seed
    def poop(self, org, foodTraits):
        stageConfigurationCopy = {}

        # Copy stage configuration 
        for stage, dictionary in foodTraits.stageConfiguration.items():
            # stage-specific variation ranges
            if stage == FoodStage.SEED:
                stageConfigurationCopy[stage] = {
                    "duration": max(1, org.traits.mutate(dictionary["duration"] , 1, 1)),
                    "nutrition": max(0, org.traits.mutate(dictionary["nutrition"] , 1, 1)),
                }
            elif stage == FoodStage.RIPE:
                stageConfigurationCopy[stage] = {
                    "duration": max(1, org.traits.mutate(dictionary["duration"] , 3, 1)),
                    "nutrition": max(0, org.traits.mutate(dictionary["nutrition"] , 5, 1)),
                }
            else:
                stageConfigurationCopy[stage] = {
                    "duration": max(1, org.traits.mutate(dictionary["duration"] , 2, 1)),
                    "nutrition": max(0, org.traits.mutate(dictionary["nutrition"] , 2, 1)),
                }
        
        food = Food(
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
        org.simulation.world.place(food, food.position)