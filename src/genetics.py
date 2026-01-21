import random

class Genetics:
    def __init__(self, generation):
        self.generation = generation
    

    #Helper function for finding variance levels, static since used by whole class, not object instances 
    @staticmethod
    def mutate(value, variance, minimum):
        return max(value + variance*random.randint(-1,1), minimum)
        

class OrganismGenetics(Genetics):
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

    # Create traits from genetics (traits are mutable, genetics are immutable)
    def toTraits(self):
        from .traits import OrganismTraits
    
    #This calculates the genetics of the parents plus slight variation for evolution to occur
    def inheritOrganismGenetics(self, genetics1, genetics2, generation):
        if isinstance(genetics1, HerbivoreGenetics):
            return HerbivoreGenetics(
                foodDetectionRadius = self.mutate((genetics1.foodDetectionRadius + genetics2.foodDetectionRadius) // 2, 2, 1),
                predatorDetectionRadius = self.mutate((genetics1.predatorDetectionRadius + genetics2.predatorDetectionRadius) // 2, 1, 1),
                speed = self.mutate((genetics1.speed + genetics2.speed) //2, 1, 1),
                energyCapacity = self.mutate((genetics1.energyCapacity + genetics2.energyCapacity) // 2 , 10, 1),
                birthEnergy = self.mutate((genetics1.birthEnergy + genetics2.birthEnergy) // 2 , 5, 1),
                slowDownAge = self.mutate((genetics1.slowDownAge + genetics2.slowDownAge) // 2 , 3, 1),
                reproductionAge = self.mutate((genetics1.reproductionAge + genetics2.reproductionAge) // 2 , 1, 2),
                matingCallRadius = self.mutate((genetics1.matingCallRadius + genetics2.matingCallRadius) // 2 , 10, 1),
                digestionTime = self.mutate((genetics1.digestionTime + genetics2.digestionTime) // 2 , 1, 1),
                generation = generation
            )

        elif isinstance(genetics1, CarnivoreGenetics):
            return CarnivoreGenetics(
                huntingRadius = self.mutate((genetics1.huntingRadius + genetics2.huntingRadius) // 2, 2, 1),
                speed = self.mutate((genetics1.speed + genetics2.speed) //2, 1, 1),
                energyCapacity = self.mutate((genetics1.energyCapacity + genetics2.energyCapacity) // 2 , 10, 1),
                birthEnergy = self.mutate((genetics1.birthEnergy + genetics2.birthEnergy) // 2 , 5, 1),
                slowDownAge = self.mutate((genetics1.slowDownAge + genetics2.slowDownAge) // 2 , 3, 1),
                reproductionAge = self.mutate((genetics1.reproductionAge + genetics2.reproductionAge) // 2 , 1, 2),
                matingCallRadius = self.mutate((genetics1.matingCallRadius + genetics2.matingCallRadius) // 2 , 10, 1),
                digestionTime = self.mutate((genetics1.digestionTime + genetics2.digestionTime) // 2 , 1, 1),
                generation = generation
            )


class HerbivoreGenetics(OrganismGenetics):
    def __init__(self, foodDetectionRadius, predatorDetectionRadius, **kwargs):
        super().__init__(**kwargs)
        self.foodDetectionRadius = foodDetectionRadius
        self.predatorDetectionRadius = predatorDetectionRadius
    
    def toTraits(self):
        from .traits import HerbivoreTraits
        return HerbivoreTraits(
            foodDetectionRadius=self.foodDetectionRadius,
            predatorDetectionRadius=self.predatorDetectionRadius,
            speed=self.speed,
            energyCapacity=self.energyCapacity,
            birthEnergy=self.birthEnergy,
            slowDownAge=self.slowDownAge,
            reproductionAge=self.reproductionAge,
            matingCallRadius=self.matingCallRadius,
            digestionTime=self.digestionTime,
            generation=self.generation
        )


class CarnivoreGenetics(OrganismGenetics):
    def __init__(self, huntingRadius, **kwargs):
        super().__init__(**kwargs)
        self.huntingRadius = huntingRadius
    
    def toTraits(self):
        from .traits import CarnivoreTraits
        return CarnivoreTraits(
            huntingRadius=self.huntingRadius,
            speed=self.speed,
            energyCapacity=self.energyCapacity,
            birthEnergy=self.birthEnergy,
            slowDownAge=self.slowDownAge,
            reproductionAge=self.reproductionAge,
            matingCallRadius=self.matingCallRadius,
            digestionTime=self.digestionTime,
            generation=self.generation
        )