class Traits:
    def __init__(self, slowDownAge, generation):
        self.slowDownAge = slowDownAge
        self.generation = generation
        

class OrganismTraits(Traits):
    def __init__(self, detectionRadius, speed, energyCapacity, slowDownAge, reproductionAge, matingCallRadius, generation):
        super().__init__(slowDownAge, generation)
        self.detectionRadius = detectionRadius
        self.speed = speed
        self.energyCapacity = energyCapacity
        self.energyConsumption = speed /2
        self.reproductionAge = reproductionAge
        self.matingCallRadius = matingCallRadius
        self.status = "Idle"

class FoodTraits(Traits):
    def __init__(self, slowDownAge, generation, nutritionValue):
        super().__init__(slowDownAge, generation)
        self.nutritionValue = nutritionValue