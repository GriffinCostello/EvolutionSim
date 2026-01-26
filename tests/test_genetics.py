import pytest
import random
from src.genetics import Genetics, OrganismGenetics, HerbivoreGenetics, CarnivoreGenetics


def test_mutate_increases_value(self):
    random.seed(42)
    base_value = 10
    variance = 2
    minimum = 1

    results = []
    for _ in range(100):
        random.seed()
        results.append(Genetics.mutate(base_value, variance, minimum))
        
    assert max(results) > base_value, "Mutation should be able to increase values"
    

def test_mutate_decreases_value(self):
    random.seed(42)
    base_value = 10
    variance = 2
    minimum = 1
        
    results = []
    for _ in range(100):
        random.seed()
        results.append(Genetics.mutate(base_value, variance, minimum))
        
    assert min(results) < base_value, "Mutation should be able to decrease values"
    

def test_mutate_respects_minimum(self):
    minimum = 5
    base_value = 6
    variance = 100
        
    results = []
    for _ in range(50):
        results.append(Genetics.mutate(base_value, variance, minimum))
        
    assert all(val >= minimum for val in results), "Mutated values should never go below minimum"