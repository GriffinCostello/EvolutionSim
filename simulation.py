import numpy as np
import simpy as simpy
import random
import math
import sys


class Simulation:
    def __init__(self, worldsize):
        self.env = simpy.Environment()
        self.worldSize = worldsize
        self.world = self.initWorld()
        self.organismList = []
        self.childCounter = 0
        self.generation = 1


    def initWorld(self):
        world = np.empty((self.worldSize, self.worldSize), dtype=object)
        world.fill(None)
        numPoints = (self.worldSize * self.worldSize) // 800  # approx 1 every 800 spaces

        # pick random coordinates
        xs = np.random.randint(0, self.worldSize, numPoints)
        ys = np.random.randint(0, self.worldSize, numPoints)
        world[xs, ys] = Food(pos=Position(x=xs, y=ys))

        print(world)
        return world


    def run(self, ticks):
        self.env.run(until=ticks)


class Traits:
    def __init__(self, detectionRadius, speed, energy, energyCapacity, slowDownAge, reproductionAge, matingCallRadius):
        self.detectionRadius = detectionRadius
        self.speed = speed
        self.energy = energy
        self.energyCapacity = energyCapacity
        self.energyConsumption = speed /2
        self.slowDownAge = slowDownAge
        self.reproductionAge = reproductionAge
        self.matingCallRadius = matingCallRadius
        self.status = "Idle"


class Actions:
    def __init__(self, organism: Orgnanism):
        self.org = organism


    def decideNextAction(self):
        if self.org.energy > self.org.energyCapacity * 0.7:
            if(self.org.age >= self.org.reproductionAge):
                return "Mate"

        closestFood = self.org.actions.scanForFood()
        if closestFood:
            return "LookForFood"
        else:
            return "Wander"


    def scanForFood(self):
        xMin = max(self.org.position.x - self.org.detectionRadius, 0)
        xMax = min(self.org.position.x + self.org.detectionRadius + 1, self.org.sim.worldSize)
        yMin = max(self.org.position.y - self.org.detectionRadius, 0)
        yMax = min(self.org.position.y + self.org.detectionRadius + 1, self.org.sim.worldSize)

        # Slice region around the organism
        area = self.org.sim.world[xMin:xMax, yMin:yMax]
        # Find actual coordinates of food
        foodPositions = np.argwhere(area != None) 
        if len(foodPositions) == 0:
            return None  # No food found

        # Convert to world coordinates
        foodGlobal = [(xMin + foodX, yMin + foodY) for foodX, foodY in foodPositions]

        # Compute closest food by distance
        closest = min(foodGlobal, key=lambda pos: (pos[0]-self.org.position.x)**2 + (pos[1]-self.org.position.y)**2)
        return closest 

    
    def moveTowards(self, target):
        targetX, targetY = target
        if self.org.position.x < targetX:
            if(self.org.position.x + self.org.speed > targetX): #if this step would overshoot
                self.org.position.x = targetX               #then just go to target
            else:
                self.org.position.x += self.org.speed

        elif self.org.position.x > targetX:
            if(self.org.position.x - self.org.speed < targetX):
                self.org.position.x = targetX
            else:
                self.org.position.x -= self.org.speed

        if self.org.position.y < targetY:
            if(self.org.position.y + self.org.speed > targetY):
                self.org.position.y = targetY
            else:
                self.org.position.y += self.org.speed

        elif self.org.position.y > targetY:
            if(self.org.position.y - self.org.speed < targetY):
                self.org.position.y = targetY
            else:
                self.org.position.y -= self.org.speed

        self.org.energy = max(self.org.energy - self.org.energyConsumption, 0)


    def eatFood(self, foodPos):
        foodX, foodY = foodPos
        if self.org.sim.world[foodX, foodY] is not None:
            self.org.sim.world[foodX, foodY] = None  # Remove food from the world
            print(f"{self.org.name} ate food at ({foodX}, {foodY})")
        else:
            print(f"{self.org.name} can't find food to eat at this position.")

        self.org.energy = min(self.org.energy + 50, self.org.energyCapacity)  # Gain energy


    def matingCall(self):
        print(f"{self.org.name} is making a mating call!")

        for otherOrganism in self.org.sim.organismList:
            if otherOrganism == self.org:
                continue
            if otherOrganism.age < otherOrganism.reproductionAge:
                continue 
            distance = self.org.position.distanceTo(otherOrganism.position)

            if distance <= self.org.matingCallRadius:
                print(f"{otherOrganism.name} heard the mating call from {self.org.name}!")
                position = (otherOrganism.position.x, otherOrganism.position.y)
                self.org.actions.moveTowards(position)
                print(f"{otherOrganism.name} moved towards {self.org.name} for mating.")
                if distance <= self.org.speed + otherOrganism.speed and otherOrganism.energy > 50 and self.org.energy > 50:
                    self.org.actions.mate(otherOrganism)

    def mate(self, otherOrganism):
        org1 = self.org
        org2 = otherOrganism
        distance = org1.position.distanceTo(org2.position)
        print(f"{org1.name} and {org2.name} have mated at distance {org1.position.asTuple()}!")
        org1.energy = max(org1.energy - org1.energyCapacity//3, 0)
        org2.energy = max(org2.energy - org2.energyCapacity//3, 0)
        org1.actions.reproduce(org2)


    def reproduce(self, otherParent):
        parent1 = self.org
        parent2 = otherParent

        parent1.sim.childCounter += 1
        childName = "Gen2_" + str(parent1.sim.childCounter)
        childTraits = Traits(
            detectionRadius = (parent1.detectionRadius + parent2.detectionRadius) // 2 + 2*random.choice([-1, 1]),
            speed = (parent1.speed + parent2.speed) //2 + 1*random.choice([-1, 1]),
            energy = (parent1.energyCapacity //3 + parent2.energyCapacity //3) // 2, #takse a third of parents' energy capacity
            energyCapacity = (parent1.energyCapacity + parent2.energyCapacity) // 2 + 10*random.choice([-1, 1]),
            slowDownAge = (parent1.slowDownAge + parent2.slowDownAge) // 2 + 3*random.choice([-1, 1]),
            reproductionAge = (parent1.reproductionAge + parent2.reproductionAge) // 2 + 1*random.choice([-1, 1]),
            matingCallRadius = (parent1.matingCallRadius + parent2.matingCallRadius) // 2 + 10*random.choice([-1, 1])
        )

        child = Organism(
            name = childName, 
            species = "Lion", 
            age = 0, 
            position = Position(
                x = (parent1.position.x + parent2.position.x) // 2,
                y = (parent1.position.y + parent2.position.y) // 2
            ),
            traits = childTraits,
            sim = parent1.sim
        )
        parent1.sim.organismList.append(child)
        print(f"{parent1.name} and {parent2.name} have reproduced to create {child.name}!")
    
    
class Organism:
    def __init__(self, name, species, age, position: Position, traits: Traits, sim):
        self.name = name
        self.species = species
        self.age = age
        
        self.position = position

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

        self.actions = Actions(self)

        self.live = self.env.process(self.live())


    def tick(self):
        self.age += 1
        if self.age == self.slowDownAge:
            self.speed = max(self.speed - 1, 1)
            self.slowDownAge += (self.slowDownAge // 2)
    
        self.energy = max(self.energy - self.energyConsumption, 0)  # Decrease energy each tick


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

            nextAction = self.actions.decideNextAction()
            match nextAction:
                case "Mate":
                    self.actions.matingCall()
                    self.status = "Mating"

                case "LookForFood":
                    closestFood = self.actions.scanForFood()
                    self.actions.moveTowards(closestFood)
                    if (self.position.x, self.position.y) == closestFood:
                        self.actions.eatFood(closestFood)
                    self.status = "Hunting"       

                case "Wander":
                    dx, dy = random.choice([(self.speed,0),(-self.speed,0),(0,self.speed),(0,-self.speed)])
                    self.position.x = (self.position.x + dx) % self.sim.worldSize
                    self.position.y = (self.position.y + dy) % self.sim.worldSize
                    self.status = "Wandering"
            
            yield self.env.timeout(1)


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distanceTo(self, otherPos):
        return math.sqrt((self.x - otherPos.x)**2 + (self.y - otherPos.y)**2)

    def asTuple(self):
        return (int(self.x), int(self.y))

class Food:
    def __init__(self, pos: Position):
        self.pos = pos


def main():
    sim = Simulation(worldsize=1000)

    position = Position(
        x=np.random.randint(0, sim.worldSize),
        y=np.random.randint(0, sim.worldSize)
    )

    genOneTraits = Traits(
        detectionRadius = 20,
        speed = 5,
        energy = 50,
        energyCapacity = 150,
        slowDownAge = 30,
        reproductionAge = 20,
        matingCallRadius = 200
    )

    for i in range(100):
        org = Organism(
            name = "Gen1_" + str(i), 
            species = "Lion", 
            age = random.randint(1, 10), 
            position = position,
            traits = genOneTraits,
            sim = sim
        )
        org.sim.organismList.append(org)

    sim.run(ticks = 50000)

if __name__ == "__main__":
    main()