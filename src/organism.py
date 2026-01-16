import random

from .actions import Actions
from .reproduction import Reproduction
from .position import Position
from .traits import *

class Organism:
    def __init__(self, name, species, age, energy, position: Position, traits: OrganismTraits, simulation: "Simulation"):
        self.name = name
        self.species = species
        self.age = age
        self.energy = energy
        
        self.position = position
        

        self.traits = traits

        # Per-organism state for when they will next slow down during their lifetime.
        self.nextSlowDownAge = self.traits.slowDownAge

        self.simulation = simulation
        self.simulation.world.validPosition(self.position)

        self.actions = Actions(self)
        self.reproduction = Reproduction(self)

        self.live = self.simulation.env.process(self.live())


    def tick(self):
        self.age += 1
        if self.age == self.nextSlowDownAge:
            self.traits.speed = max(self.traits.speed - 1, 1)
            self.traits.energyCapacity = max(self.traits.energyCapacity - 30, 100)
            if isinstance(self.traits, HerbivoreTraits):
                self.traits.foodDetectionRadius = max(self.traits.foodDetectionRadius -3, 1)
            self.nextSlowDownAge += (self.nextSlowDownAge // 2)
    
        self.energy = max(self.energy - self.traits.energyConsumption, 0)  # Decrease energy each tick


    def live(self):
        while True:
            
            self.tick()
            
            if self.energy <= 0:
                #print(f"{self.name} has run out of energy and died at age {self.age}.")
                self.simulation.statistics.logLifespan(self.age, self.species)
                self.simulation.organismList.remove(self)
                
                if len(self.simulation.organismList) == 0:
                    if not self.simulation.stopEvent.triggered:
                        self.simulation.stopEvent.succeed()

                break

            nextAction = self.actions.decideNextAction()
            match nextAction:
                case "Flee":
                    threatPosition = self.actions.scanForPredators()
                    if threatPosition:
                        self.actions.moveAwayFrom(threatPosition)
                        self.status = "Fleeing"
                case "Mate":
                    self.actions.matingCall()
                    self.status = "Mating"

                case "LookForFood":
                    if isinstance(self.traits, HerbivoreTraits):
                        bestFood = self.actions.scanForFood()
                        if bestFood:
                            self.actions.moveTowards(bestFood)
                            if (self.position.x, self.position.y) == bestFood:
                                self.actions.eatFood(bestFood)
                        self.status = "Hunting"

                    elif isinstance(self.traits, CarnivoreTraits):
                        prey = self.actions.scanForPrey()
                        if prey:
                            self.actions.moveTowards(prey.position.asTuple())
                            self.actions.eatPrey(prey)
                        self.status = "Hunting"

                case "Wander":
                    dx, dy = random.choice([(self.traits.speed,0),(-self.traits.speed,0),(0,self.traits.speed),(0,-self.traits.speed)])
                    self.position.x = (self.position.x + dx) % self.simulation.worldSize
                    self.position.y = (self.position.y + dy) % self.simulation.worldSize
                    self.status = "Wandering"
            
            yield self.simulation.env.timeout(1)