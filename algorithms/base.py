from models import City
from typing import List
from copy import deepcopy
from models import Tour


class Algorithm:

    def __init__(self, cities: List[City], cost_map):
        self.cities = deepcopy(cities)
        self.cost_map = cost_map
        self.best: Tour = Tour(0, cost_map)

    def get_best(self):
        return deepcopy(self.best)

    def iterate(self):
        return NotImplementedError()
