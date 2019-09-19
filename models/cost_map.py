from typing import List

from .city import City


class CostMap:

    def __init__(self, cities: List[City]):
        self._cost_map = {}
        for i in range(len(cities)):
            for j in range(len(cities)):
                src_city = cities[i]
                dest_city = cities[j]
                self._cost_map[(i, j)] = src_city.get_distance_to(dest_city)

    def get_distance(self, src_idx, dest_idx):
        return self._cost_map[(src_idx, dest_idx)]
