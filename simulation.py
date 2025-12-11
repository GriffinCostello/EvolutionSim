import numpy as np
import simpy as simpy
import random
import math
import sys


class Simulation:
    def __init__(self, worldsize):
        self.env = simpy.Environment()
        self.worldSize = worldsize
        self.world = self.initMap()
        self.organismList = []
        self.childCounter = 0

    def initMap(self):
        map = np.zeros((self.worldSize, self.worldSize), dtype=int)
        numPoints = (self.worldSize * self.worldSize) // 800  # approx 1 every 800 spaces

        # pick random coordinates
        xs = np.random.randint(0, self.worldSize, numPoints)
        ys = np.random.randint(0, self.worldSize, numPoints)

        map[xs, ys] = 1

        return map

    def run(self, ticks):
        self.env.run(until=ticks)

class Traits:
    def __init__(self, detectionRadius, speed, energy, slowDownAge, reproductionAge, matingCallRadius):
        self.detectionRadius = detectionRadius
        self.speed = speed
        self.energy = energy
        self.energyCapacity = energy*2.5
        self.energyConsumption = speed /2
        self.slowDownAge = slowDownAge
        self.reproductionAge = reproductionAge
        self.matingCallRadius = matingCallRadius
        self.status = "Idle"


class Organism:
    def __init__(self, name, species, age, posX , posY, traits: Traits, sim):
        self.name = name
        self.species = species
        self.age = age
        self.posX = posX
        self.posY = posY

        self.detectionRadius = traits.detectionRadius
        self.speed = traits.speed
        self.energy = traits.energy
        self.energyCapacity = traits.energyCapacity
        self.energyConsumption = traits.energyConsumption
        self.slowDownAge = traits.slowDownAge
        self.reproductionAge = traits.reproductionAge
        self.matingCallRadius = traits.matingCallRadius

        self.sim = sim
        self.env = sim.env
        self.world = sim.world

        self.live = self.env.process(self.live())


    def tick(self):
        self.age += 1
        if self.age == self.slowDownAge:
            self.speed = max(self.speed - 1, 1)
            self.slowDownAge += (self.slowDownAge // 2)
    
        self.energy = max(self.energy - self.energyConsumption, 0)  # Decrease energy each tick


    def scanForFood(self, world):
        xMin = max(self.posX - self.detectionRadius, 0)
        xMax = min(self.posX + self.detectionRadius + 1, self.sim.worldSize)
        yMin = max(self.posY - self.detectionRadius, 0)
        yMax = min(self.posY + self.detectionRadius + 1, self.sim.worldSize)

        # Slice region around the organism
        area = world[xMin:xMax, yMin:yMax]
        # Find actual coordinates of food
        foodPositions = np.argwhere(area == 1) 
        if len(foodPositions) == 0:
            return None  # No food found

        # Convert to world coordinates
        foodGlobal = [(xMin + foodX, yMin + foodY) for foodX, foodY in foodPositions]

        # Compute closest food by distance
        closest = min(foodGlobal, key=lambda pos: (pos[0]-self.posX)**2 + (pos[1]-self.posY)**2)
        return closest 


    def moveTowards(self, target):
        targetX, targetY = target
        if self.posX < targetX:
            if(self.posX + self.speed > targetX): #if this step would overshoot
                self.posX = targetX               #then just go to target
            else:
                self.posX += self.speed
        elif self.posX > targetX:
            if(self.posX - self.speed < targetX):
                self.posX = targetX
            else:
                self.posX -= self.speed

        if self.posY < targetY:
            if(self.posY + self.speed > targetY):
                self.posY = targetY
            else:
                self.posY += self.speed
        elif self.posY > targetY:
            if(self.posY - self.speed < targetY):
                self.posY = targetY
            else:
                self.posY -= self.speed

        self.energy = max(self.energy - self.energyConsumption, 0)

    def eatFood(self, world, foodPos):
        foodX, foodY = foodPos
        if world[foodX, foodY] == 1:
            world[foodX, foodY] = 0  # Remove food from the world
            print(f"{self.name} ate food at ({foodX}, {foodY})")
        else:
            print(f"{self.name} can't find food to eat at this position.")

        self.energy = min(self.energy + 50, self.energyCapacity)  # Gain energy

    def matingCall(self):
        print(f"{self.name} is making a mating call!")

        for i in self.sim.organismList:
            if i == self:
                continue
            if i.age < i.reproductionAge:
                continue 
            distance = int(math.sqrt((self.posX-i.posX)**2 + (self.posY-i.posY)**2))
            if distance <= self.matingCallRadius:
                print(f"{i.name} heard the mating call from {self.name}!")
                position = (i.posX, i.posY)
                self.moveTowards(position)
                print(f"{i.name} moved towards {self.name} for mating.")
                if(distance := int(math.sqrt((self.posX - i.posX)**2 + (self.posY - i.posY)**2))) <= self.speed + i.speed:
                    mate(self, i)


    def decideNextAction(self):
        if self.energy > self.energyCapacity * 0.7:
            if(self.age >= self.reproductionAge):
                return "Mate"

        closestFood = self.scanForFood(self.world)
        if closestFood:
            return "LookForFood"
        else:
            return "Wander"


    def live(self):
        while True:
            
            self.tick()
            if self.energy <= 0:
                print(f"{self.name} has run out of energy and died at age {self.age}.")
                
                if len(self.sim.organismList) == 1:
                    print("All organisms have died. Ending simulation.")
                    sys.exit()
                self.sim.organismList.remove(self)
                break

            nextAction = self.decideNextAction()
            match nextAction:
                case "Mate":
                    self.matingCall()
                    self.status = "Mating"

                case "LookForFood":
                    closestFood = self.scanForFood(self.world)
                    self.moveTowards(closestFood)
                    if (self.posX, self.posY) == closestFood:
                        self.eatFood(self.world, closestFood)
                    self.status = "Hunting"       

                case "Wander":
                    dx, dy = random.choice([(self.speed,0),(-self.speed,0),(0,self.speed),(0,-self.speed)])
                    self.posX = (self.posX + dx) % self.sim.worldSize
                    self.posY = (self.posY + dy) % self.sim.worldSize
                    self.status = "Wandering"
            
            yield self.env.timeout(1)

def mate(org1, org2):
    if (distance := int(math.sqrt((org1.posX - org2.posX)**2 + (org1.posY - org2.posY)**2))) <= org1.speed + org2.speed:
        print(f"{org1.name} and {org2.name} have mated at distance {distance}!")
        org1.energy = max(org1.energy - 50, 0)
        org2.energy = max(org2.energy - 50, 0)
        reproduce(org1, org2)


def reproduce(parent1, parent2):
    parent1.sim.childCounter += 1
    childName = "Gen2_" + str(parent1.sim.childCounter)
    childTraits = Traits(
        detectionRadius = (parent1.detectionRadius + parent2.detectionRadius) // 2 + 2*random.choice([-1, 1]),
        speed = (parent1.speed + parent2.speed) //2 + 1*random.choice([-1, 1]),
        energy = (parent1.energy + parent2.energy) // 2 + 5*random.choice([-1, 1]),
        slowDownAge = (parent1.slowDownAge + parent2.slowDownAge) // 2 + 3*random.choice([-1, 1]),
        reproductionAge = (parent1.reproductionAge + parent2.reproductionAge) // 2 + 1*random.choice([-1, 1]),
        matingCallRadius = (parent1.matingCallRadius + parent2.matingCallRadius) // 2 + 10*random.choice([-1, 1])
    )

    childName = Organism(
        name = childName, 
        species = "Lion", 
        age = 0, 
        posX = parent1.posX, 
        posY = parent1.posY, 
        traits = childTraits,
        sim = parent1.sim
    )
    parent1.sim.organismList.append(childName)
    parent1.energy = max(parent1.energy - 30, 0)
    parent2.energy = max(parent2.energy - 30, 0)
    print(f"{parent1.name} and {parent2.name} have reproduced to create {childName.name}!")
        

def main():
    sim = Simulation(worldsize=1000)
    genOneTraits = Traits(
        detectionRadius = 20,
        speed = 5,
        energy = 50,
        slowDownAge = 30,
        reproductionAge = 20,
        matingCallRadius = 200
    )

    for i in range(100):
        org = Organism(
            name = "Gen1_" + str(i), 
            species = "Lion", 
            age = random.randint(1, 10), 
            posX = np.random.randint(0, sim.worldSize), 
            posY = np.random.randint(0, sim.worldSize), 
            traits = genOneTraits,
            sim = sim
        )
        org.sim.organismList.append(org)

    sim.run(ticks = 50000)

if __name__ == "__main__":
    main()