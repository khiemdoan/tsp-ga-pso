import re

from models import City


class DataReader:

    def __init__(self):
        self._description = ''
        self._cities = []

    def load(self, file_path):
        self._description = ''
        self._cities = []
        with open(file_path, 'r', encoding='utf-8') as in_file:
            for line in in_file:
                if not self._description:
                    match = re.match(r'COMMENT : (?P<description>(\w|\s)+)', line)
                    if match:
                        self._description = match.group('description')

                match = re.match(r'(?P<name>\d+) (?P<x>(\d|\.)+) (?P<y>(\d|\.)+)', line)
                if match:
                    name = match.group('name')
                    x = float(match.group('x'))
                    y = float(match.group('y'))
                    city = City(name, x, y)
                    self._cities.append(city)

    def get_description(self):
        return self._description

    def get_cities(self):
        return self._cities
