from .base import Algorithm
import numpy as np
from models import Tour
import random
from copy import deepcopy

number_particles = 100
W = 0.6
c1 = 0.2
c2 = 0.2


class Particle:

    def __init__(self, number_cities, cost_map):
        self._tour = None
        self.cost_map = cost_map
        self.position = np.random.rand(number_cities) * 20 - 10
        self.pbest_position = self.position
        self.pbest_value = self.get_tour().cost
        self.velocity = np.zeros(number_cities, dtype=np.float)

    def get_tour(self):
        if self._tour:
            return self._tour
        tour = Tour(0, self.cost_map)
        solution = np.argsort(np.argsort(self.position))
        for i in solution:
            tour.add(i)
        self._tour = tour
        return tour

    def move(self):
        self._tour = None
        self.position = self.position + self.velocity

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.position)


class ParticleSwarmOptimization(Algorithm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        total_cities = len(self.cities)
        self.particles = [Particle(total_cities, self.cost_map) for _ in range(number_particles)]
        self.gbest_value = float('inf')
        self.gbest_position = None

        self.set_pbest()
        self.set_gbest()

    def set_pbest(self):
        for particle in self.particles:
            fitness_cadidate = particle.get_tour().cost
            if fitness_cadidate < particle.pbest_value:
                particle.pbest_value = fitness_cadidate
                particle.pbest_position = deepcopy(particle.position)

    def set_gbest(self):
        for particle in self.particles:
            best_fitness_cadidate = particle.get_tour().cost
            if best_fitness_cadidate < self.gbest_value:
                self.gbest_value = particle.get_tour().cost
                self.gbest_position = deepcopy(particle.position)

    def move_particles(self):
        for particle in self.particles:
            new_velocity = (W * particle.velocity)\
                           + c1 * random.random() * (particle.pbest_position - particle.position)\
                           + c2 * random.random() * (self.gbest_position - particle.position)
            particle.velocity = new_velocity
            particle.move()

    def get_tour(self):
        tour = Tour(0, self.cost_map)
        solution = np.argsort(np.argsort(self.gbest_position))
        for i in solution:
            tour.add(i)
        return tour

    def iterate(self):
        self.move_particles()
        self.set_pbest()
        self.set_gbest()
        self.best = Tour(0, self.cost_map)
        solution = np.argsort(np.argsort(self.gbest_position))
        for i in solution:
            self.best.add(i)
