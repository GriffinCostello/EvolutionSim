import simpy
import numpy as np
import random
import math
import sys

from actions import Actions
from position import Position
from traits import Traits

class Organism:
    def __init__(self, name, species, position: Position, traits: OrganismTraits, sim):
        self.name = name
        self.species = species
        
        self.position = position

        self.age = traits.age
        self.detectionRadius = traits.detectionRadius
        self.speed = traits.speed
        self.energy = traits.energy
        self.energyCapacity = traits.energyCapacity
        self.energyConsumption = traits.energyConsumption
        self.slowDownAge = traits.slowDownAge
        self.reproductionAge = traits.reproductionAge
        self.matingCallRadius = traits.matingCallRadius
        self.generation = traits.generation

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
            if len(self.sim.organismList) == 1:
                    print("All alone")
                    sys.exit()
            if self.energy <= 0:
                print(f"{self.name} has run out of energy and died at age {self.age}.")
                
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