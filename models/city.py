import math

from scipy.spatial.distance import euclidean


class City:

    def __init__(self, name, x, y):
        self._name = name
        self._x = x
        self._y = y

    def __repr__(self):
        return f'city_{self._name}'

    def __str__(self):
        return self.__repr__()

    @property
    def name(self):
        return self._name

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def get_distance_to(self, point):
        return euclidean([self.x, self.y], [point.x, point.y])
