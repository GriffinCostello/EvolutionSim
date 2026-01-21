import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

class Statistics:
    def __init__(self):
        self.traitLog = defaultdict(lambda: defaultdict(list))
        self.lifeSpan = [1] # list to keep track of lifespans of dead organisms, base value 1 to prevent division by zero
        self.lifeSpanBySpecies = defaultdict(lambda: [1])
        

    def logGenetics(self, traitName, generation, value):
        self.traitLog[traitName][generation].append(value)


    def logLifespan(self, lifespan, species=None):
        self.lifeSpan.append(lifespan)
        if species is not None:
            self.lifeSpanBySpecies[species].append(lifespan)


    #Prints graph for average speed per generation
    def plotGeneticsEvolution(self, traitName):
        if traitName not in self.traitLog:
            print(f"No trait: '{traitName}'")
            return

        generations = sorted(self.traitLog[traitName].keys())
        medians = [
            np.median(self.traitLog[traitName][g])
            for g in generations
        ]

        plt.figure()
        plt.plot(generations, medians, marker='o')
        plt.xlabel("Generation")
        plt.ylabel(f"Median {traitName}")
        plt.title(f"Herbivore {traitName} Evolution")
        plt.show()
        