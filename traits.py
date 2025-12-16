class Traits:
    def __init__(self, age, slowDownAge, generation):
        self.age = age
        self.slowDownAge = slowDownAge
        self.generation = generation
        

class OrganismTraits(Traits):
    def __init__(self, age, detectionRadius, speed, energy, energyCapacity, slowDownAge, reproductionAge, matingCallRadius, generation):
        super().__init__(age, slowDownAge, generation)
        self.detectionRadius = detectionRadius
        self.speed = speed
        self.energy = energy
        self.energyCapacity = energyCapacity
        self.energyConsumption = speed /2
        self.reproductionAge = reproductionAge
        self.matingCallRadius = matingCallRadius
        self.status = "Idle"

class FoodTraits(Traits):
    def __init__(self, age, slowDownAge, generation, nutritionValue):
        super().__init__(age, slowDownAge, generation)
        self.nutritionValue = nutritionValue