class Traits:
    def __init__(self, detectionRadius, speed, energy, energyCapacity, slowDownAge, reproductionAge, matingCallRadius, generation):
        self.detectionRadius = detectionRadius
        self.speed = speed
        self.energy = energy
        self.energyCapacity = energyCapacity
        self.energyConsumption = speed /2
        self.slowDownAge = slowDownAge
        self.reproductionAge = reproductionAge
        self.matingCallRadius = matingCallRadius
        self.generation = generation
        self.status = "Idle"