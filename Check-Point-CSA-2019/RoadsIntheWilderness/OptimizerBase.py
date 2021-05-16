import numpy as np
import typing
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import *

from Coordinate import Coordinate
from HexagonMap import HexagonMap
from shared_structs import City


class RoadOptimizerBase(object):
    def __init__(self, hm: HexagonMap):
        self.hm = hm
        self.city_indices = [self.coordinate_to_index(c.coordinate) for c in self.hm.cities]
        self.costs, self.paths = shortest_path(self._create_cost_graph(),
                                               # method='auto', directed=True,
                                               method='D', directed=True, return_predecessors=True,
                                               unweighted=False, overwrite=False,
                                               indices=self.city_indices)

    def _create_cost_graph(self) -> csr_matrix:
        graph = np.zeros((self.hm.width ** 2, self.hm.height ** 2), dtype=int)
        for node in self.hm.get_all_nodes():
            graph[self.coordinate_to_index(node)][self.coordinate_to_index(node)] = 0
            for neighbor in self.hm.get_neighbors(node):
                graph[self.coordinate_to_index(node)][self.coordinate_to_index(neighbor)] = self.hm.get_cost(neighbor)
        return csgraph_from_dense(graph)

    def coordinate_to_index(self, coord: Coordinate) -> int:
        return coord.x * self.hm.width + coord.y

    def index_to_coordinate(self, index: int) -> Coordinate:
        return Coordinate(index // self.hm.width, index % self.hm.width)

    def get_index_in_city_indices(self, city_index: int) -> int:
        return self.city_indices.index(city_index)

    def get_path(self, origin_city_index: int, dst_city_index: int) -> typing.List:
        origin_index_in_city_indices = self.get_index_in_city_indices(origin_city_index)
        path = [dst_city_index]
        dst = dst_city_index
        while self.paths[origin_index_in_city_indices, dst] != -9999:
            path.append(self.paths[origin_index_in_city_indices, dst])
            dst = self.paths[origin_index_in_city_indices, dst]

        return path[::-1]

    def get_roads_for_city(self, origin_city: City):
        raise NotImplementedError("Implement me")

    def coordinate_to_index(self, coord: Coordinate) -> int:
        return coord.x * self.hm.width + coord.y

    def index_to_coordinate(self, index: int) -> Coordinate:
        return Coordinate(index // self.hm.width, index % self.hm.width)
