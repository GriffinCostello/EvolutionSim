from enum import Enum, auto
import random

class Traits:
    def __init__(self, generation):
        self.generation = generation
        

class OrganismTraits(Traits):
    def __init__(self, speed, energyCapacity, birthEnergy, slowDownAge, reproductionAge, matingCallRadius, digestionTime, generation):
        super().__init__(generation)
        self.speed = speed
        self.energyCapacity = energyCapacity
        self.birthEnergy = birthEnergy
        self.energyConsumption = speed / 2  
        self.reproductionAge = reproductionAge
        self.slowDownAge = slowDownAge
        self.matingCallRadius = matingCallRadius
        self.digestionTime = digestionTime
        self.status = "Idle"


class HerbivoreTraits(OrganismTraits):
    def __init__(self, detectionRadius, **kwargs):
        super().__init__(**kwargs)
        self.detectionRadius = detectionRadius


class CarnivoreTraits(OrganismTraits):
    def __init__(self, huntingRadius, **kwargs):
        super().__init__(**kwargs)
        self.huntingRadius = huntingRadius


class FoodTraits(Traits):
    def __init__(self,generation, stageConfiguration):
        super().__init__(generation)

        self.stageConfiguration = stageConfiguration

        self.stageDurations = {}
        self.nutritionalValue = {}
        
        durationCalculator = 0
        for stage, dictionary in stageConfiguration.items():
            duration = dictionary["duration"]
            self.stageDurations[stage] = (durationCalculator, durationCalculator + duration)  #Adds duration to length so it can be compared to age
            self.nutritionalValue[stage] = dictionary["nutrition"]
            durationCalculator += duration
            
        self.totalLifespan = durationCalculator
        


class FoodStage(Enum):
    SEED = auto()
    RIPENING = auto()
    RIPE = auto()
    ROTTING = auto()
    ROTTEN = auto()