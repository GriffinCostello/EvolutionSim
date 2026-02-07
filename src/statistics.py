import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

class Statistics:
    def __init__(self):
        self.traitLog = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        self.traitLogHerbivore = self.traitLog['Herbivore']
        self.traitLogCarnivore = self.traitLog['Carnivore']
        self.lifeSpan = [1] # list to keep track of lifespans of dead organisms, base value 1 to prevent division by zero
        self.lifeSpanBySpecies = defaultdict(lambda: [1])
        

    def logGeneticsHerbivore(self, traitName, generation, value):
        self.traitLogHerbivore[traitName][generation].append(value)

    def logGeneticsCarnivore(self, traitName, generation, value):
        self.traitLogCarnivore[traitName][generation].append(value)


    def logLifespan(self, lifespan, species=None):
        self.lifeSpan.append(lifespan)
        if species is not None:
            self.lifeSpanBySpecies[species].append(lifespan)


    #Prints graph for average speed per generation
    def plotGeneticsEvolution(self, traitName, species):
        if species == "Herbivore":
            traitLog = self.traitLogHerbivore
        elif species == "Carnivore":
            traitLog = self.traitLogCarnivore
            
        if traitName not in traitLog:
            print(f"No trait: '{traitName}'")
            return

        generations = sorted(traitLog[traitName].keys())
        medians = [
            np.median(traitLog[traitName][g])
            for g in generations
        ]

        plt.figure()
        plt.plot(generations, medians, marker='o')
        plt.xlabel("Generation")
        plt.ylabel(f"Median {traitName}")
        plt.title(f"{species} {traitName} Evolution")
        plt.show()
        