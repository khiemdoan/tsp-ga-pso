from copy import deepcopy
from typing import List

from .city import City


class Tour:

    def __init__(self, number_cities, cost_map):
        self._order = []
        self.cost_map = cost_map
        self._cost = None

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        city_names = [str(city) for city in self._order]
        cities_str = ', '.join(city_names)
        return f'{self._cost} - ({cities_str})'

    def __getitem__(self, index):
        return self._order[index]

    def __contains__(self, item):
        return item in self._order

    def __setitem__(self, index, value):
        self._cost = None
        self._order[index] = value

    def add(self, city_index):
        self._cost = None
        self._order.append(city_index)

    def __len__(self):
        return len(self._order)

    def is_valid(self):
        total_cities = len(self._order)
        total_distinct_cities = len(set([city for city in self._order if city is not None]))
        return total_cities == total_distinct_cities

    @property
    def cost(self):
        if self._cost:
            return self._cost

        self._cost = 0
        for i in range(len(self._order)):
            src_idx = self._order[i]
            dest_idx = self._order[(i + 1) % len(self._order)]
            cost = self.cost_map.get_distance(src_idx, dest_idx)
            self._cost += cost
        return self._cost

    @property
    def order(self):
        return self._order

    def clone(self):
        return deepcopy(self)
