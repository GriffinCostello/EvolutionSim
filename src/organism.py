import random

from .actions import Actions
from .reproduction import Reproduction
from .position import Position
from .traits import *
from .genetics import *

class Organism:
    def __init__(self, name, species, age, energy, position: Position, genetics: "OrganismGenetics", simulation: "Simulation", traits: OrganismTraits = None):
        self.name = name
        self.species = species
        self.age = age
        self.energy = energy
        
        self.position = position
        
        self.genetics = genetics
        
        #Creates traits from genetics when organism is created
        self.traits = genetics.toTraits()


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
            if isinstance(self.genetics, HerbivoreGenetics):
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
                if isinstance(self.genetics, HerbivoreGenetics):
                    self.simulation.herbivoreList.remove(self)
                elif isinstance(self.genetics, CarnivoreGenetics):
                    self.simulation.carnivoreList.remove(self)
                
                if len(self.simulation.organismList) == 0:
                    if not self.simulation.stopEvent.triggered:
                        self.simulation.stopEvent.succeed()

                break

            nextAction, target = self.actions.decideNextAction()
            match nextAction:
                case "Flee":
                    if target:
                        self.actions.moveAwayFrom(target)
                case "Mate":
                    self.actions.matingCall()

                case "LookForFood":
                    if isinstance(self.genetics, HerbivoreGenetics):
                        if target:
                            self.actions.moveTowards(target)
                            if (self.position.x, self.position.y) == target:
                                self.actions.eatFood(target)

                    elif isinstance(self.genetics, CarnivoreGenetics):
                        if target:
                            self.actions.moveTowards(target.position.asTuple())
                            self.actions.eatPrey(target)

                case "Wander":
                    dx, dy = random.choice([(self.traits.speed,0),(-self.traits.speed,0),(0,self.traits.speed),(0,-self.traits.speed)])
                    self.position.x = (self.position.x + dx) % self.simulation.worldSize
                    self.position.y = (self.position.y + dy) % self.simulation.worldSize
            
            yield self.simulation.env.timeout(1)