from enum import Enum, auto
import random

class Traits:
    def __init__(self, generation):
        self.generation = generation
    

    #Helper function for finding variance levels, static since used by whole class, not object instances 
    @staticmethod
    def mutate(value, variance, minimum):
        return max(value + variance*random.randint(-1,1), minimum)
        

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

    
    #This calculates the traits of the parents plus slight variation for evolution to occur
    def inheritOrganismTraits(self, traits1, traits2, generation):
        if isinstance(traits1, HerbivoreTraits):
            return HerbivoreTraits(
                foodDetectionRadius = self.mutate((traits1.foodDetectionRadius + traits2.foodDetectionRadius) // 2, 2, 1),
                predatorDetectionRadius = self.mutate((traits1.predatorDetectionRadius + traits2.predatorDetectionRadius) // 2, 1, 1),
                speed = self.mutate((traits1.speed + traits2.speed) //2, 1, 1),
                energyCapacity = self.mutate((traits1.energyCapacity + traits2.energyCapacity) // 2 , 10, 1),
                birthEnergy = self.mutate((traits1.birthEnergy + traits2.birthEnergy) // 2 , 5, 1),
                slowDownAge = self.mutate((traits1.slowDownAge + traits2.slowDownAge) // 2 , 3, 1),
                reproductionAge = self.mutate((traits1.reproductionAge + traits2.reproductionAge) // 2 , 1, 2),
                matingCallRadius = self.mutate((traits1.matingCallRadius + traits2.matingCallRadius) // 2 , 10, 1),
                digestionTime = self.mutate((traits1.digestionTime + traits2.digestionTime) // 2 , 1, 1),
                generation = generation
            )

        elif isinstance(traits1, CarnivoreTraits):
            return CarnivoreTraits(
                huntingRadius = self.mutate((traits1.huntingRadius + traits2.huntingRadius) // 2, 2, 1),
                speed = self.mutate((traits1.speed + traits2.speed) //2, 1, 1),
                energyCapacity = self.mutate((traits1.energyCapacity + traits2.energyCapacity) // 2 , 10, 1),
                birthEnergy = self.mutate((traits1.birthEnergy + traits2.birthEnergy) // 2 , 5, 1),
                slowDownAge = self.mutate((traits1.slowDownAge + traits2.slowDownAge) // 2 , 3, 1),
                reproductionAge = self.mutate((traits1.reproductionAge + traits2.reproductionAge) // 2 , 1, 2),
                matingCallRadius = self.mutate((traits1.matingCallRadius + traits2.matingCallRadius) // 2 , 10, 1),
                digestionTime = self.mutate((traits1.digestionTime + traits2.digestionTime) // 2 , 1, 1),
                generation = generation
            )


class HerbivoreTraits(OrganismTraits):
    def __init__(self, foodDetectionRadius, predatorDetectionRadius, **kwargs):
        super().__init__(**kwargs)
        self.foodDetectionRadius = foodDetectionRadius
        self.predatorDetectionRadius = predatorDetectionRadius


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