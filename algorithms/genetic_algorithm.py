from .base import Algorithm
import random
from copy import deepcopy
from models import Tour
from typing import List, Tuple

n_population = 100
CXPB = 0.95
MUTPB = 0.1


class GeneticAlgorithm(Algorithm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.population: List[Tour] = []
        self.init_population()

    def init_population(self):
        cities = [idx for idx in range(len(self.cities))]
        for _ in range(n_population):
            random.shuffle(cities)
            tour = Tour(len(cities), self.cost_map)
            tour[:] = cities
            self.population.append(tour)

        self.population = sorted(self.population, key=lambda x: x.cost)
        self.best = deepcopy(self.population[0])

    def iterate(self):
        random.shuffle(self.population)

        offsprings = list()
        for i, (ind1, ind2) in enumerate(zip(self.population[::2], self.population[1::2])):
            if random.random() > CXPB:
                continue
            offspring1, offspring2 = self.crossover(ind1, ind2)
            offsprings.append(offspring1)
            offsprings.append(offspring2)

        for i, mutant in enumerate(offsprings):
            if random.random() > MUTPB:
                continue
            offsprings[i] = self._mutate(mutant)

        new_population = self.population + offsprings
        new_population = sorted(new_population, key=lambda x: x.cost)
        self.population[:n_population//2] = new_population[:n_population//2]
        self.population[n_population//2:] = random.choices(
            new_population[n_population//2:],
            k=n_population-n_population//2)

        assert self.best.cost >= self.population[0].cost, 'Tien hoa khong thanh cong'
        self.best = deepcopy(self.population[0])

    def _mutate(self, individual: Tour):
        individual = deepcopy(individual)
        idx1 = random.randint(0, len(self.cities) - 1)
        idx2 = random.randint(0, len(self.cities) - 1)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
        return individual

    def select(self, population):
        offspring = list()
        offspring.append(population[0].clone())

        for _ in range(1, len(population)):
            idx = random.randint(0, len(population) - 1)
            offspring.append(population[idx].clone())
        return offspring

    def crossover(self, ind1: Tour, ind2: Tour) -> Tuple[Tour, Tour]:
        child1 = Tour(len(ind1), ind1.cost_map)
        child2 = Tour(len(ind1), ind1.cost_map)

        idx = random.randint(0, len(ind1) - 1)

        for i in range(idx):
            child1.add(ind1[i])
            child2.add(ind2[i])

        for i in range(idx, len(ind1)):
            if ind2[i] not in child1:
                child1.add(ind2[i])
            if ind1[i] not in child2:
                child2.add(ind1[i])

        for i in range(len(ind1)):
            if ind1[i] not in child1:
                child1.add(ind1[i])
            if ind2[i] not in child2:
                child2.add(ind2[i])

        return child1, child2
