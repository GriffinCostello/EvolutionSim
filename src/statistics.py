import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

class Statistics:
    def __init__(self):
        self.geneticLog = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        self.geneticLogHerbivore = self.geneticLog['Herbivore']
        self.geneticLogCarnivore = self.geneticLog['Carnivore']
        self.lifeSpan = [1] # list to keep track of lifespans of dead organisms, base value 1 to prevent division by zero
        self.lifeSpanBySpecies = defaultdict(lambda: [1])
        

    def logGeneticsHerbivore(self, traitName, generation, value):
        self.geneticLogHerbivore[traitName][generation].append(value)

    def logGeneticsCarnivore(self, traitName, generation, value):
        self.geneticLogCarnivore[traitName][generation].append(value)


    def logLifespan(self, lifespan, species=None):
        self.lifeSpan.append(lifespan)
        if species is not None:
            self.lifeSpanBySpecies[species].append(lifespan)


    #Prints graph for average speed per generation
    def plotGeneticsEvolution(self, geneticName, species):
        if species == "Herbivore":
            geneticLog = self.geneticLogHerbivore
        elif species == "Carnivore":
            geneticLog = self.geneticLogCarnivore
            
        if geneticName not in geneticLog:
            print(f"No trait: '{geneticName}'")
            return

        generations = sorted(geneticLog[geneticName].keys())
        medians = [
            np.median(geneticLog[geneticName][g])
            for g in generations
        ]

        plt.figure()
        plt.plot(generations, medians, marker='o')
        plt.xlabel("Generation")
        plt.ylabel(f"Median {geneticName}")
        plt.title(f"{species} {geneticName} Evolution")
        plt.show()
        