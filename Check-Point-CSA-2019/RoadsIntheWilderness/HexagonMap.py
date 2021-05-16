import re
import typing

from Coordinate import Coordinate
from shared_structs import Terrain, Product, City


class HexagonMap(object):
    NEIGHBORS = [
        [(1, -1), (-1, -1), (0, 1), (1, 0), (0, -1), (-1, 0)],  # Even
        [(0, 1), (-1, 0), (1, 0), (0, -1), (-1, 1), (1, 1)]  # Odd
    ]

    def __init__(self, cost_map: typing.Dict):
        self.initialized = False
        self.map = []
        self.cities = []
        self.cost_map = cost_map

    def from_data_file(self, path: str):
        if self.initialized:
            raise RuntimeError("Map already initialized")
        try:
            with open(path) as f:
                if f.readline() != "Map terrain:\n":
                    raise RuntimeError("Incorrect format: Expected map terrain")

                line = f.readline()
                while line != "Cities:\n":
                    if line != "\n":
                        line = line.strip("[],\n")
                        self.map.append(list(
                            map(lambda x: Terrain[x.upper()], line.split(", "))))
                    line = f.readline()  # TODO: check what's inside map

                assert (line == "Cities:\n")
                city_regex = re.compile(r'^\((\d+),\s(\d+)\),\s([\w, ]+)$')

                while line != "":
                    match = city_regex.match(line.rstrip())
                    if match:
                        coord = Coordinate(int(match.group(1)),
                                           int(match.group(2)))
                        products = tuple(map(lambda x: Product[x.upper()],
                                             match.group(3).split(", ")))
                        city = City(coord, products)
                        self.cities.append(city)
                    line = f.readline()

            self.width = len(self.map[0])
            self.height = len(self.map)
            self.initialized = True
        except RuntimeError as e:
            raise e
        except Exception as e:
            raise RuntimeError("Error parsing data file: {}".format(e))

    def get_neighbors(self, coordinate: Coordinate) -> typing.List:
        """Return the neighbors of a given coordinate"""
        res = []
        for (dx, dy) in self.NEIGHBORS[coordinate.x % 2]:
            new_x = coordinate.x + dx
            new_y = coordinate.y + dy
            if (0 <= new_x < self.height) and (0 <= new_y < self.width):
                res.append(Coordinate(new_x, new_y))
        return res

    def get_all_nodes(self) -> typing.Generator[Coordinate, None, None]:
        """Return all nodes in graph"""
        for x in range(self.width):
            for y in range(self.height):
                yield Coordinate(x, y)

    def get_cost(self, coordinate: Coordinate) -> int:
        """Return the cost of a given coordinate"""
        return self.cost_map[self.map[coordinate.x][coordinate.y]]
