import copy
import math
import sys
import typing

from HexagonMap import HexagonMap
from OptimizerBase import RoadOptimizerBase
from shared_structs import Product, City


class RoadOptimizerV1(RoadOptimizerBase):
    def __init__(self, hm: HexagonMap):
        super().__init__(hm)

        # Create a list of length len(Product).
        # Each item is a list of all the
        # cities that have the matching product.
        self.cities_per_product = [[] for _ in range(len(Product))]
        for city in hm.cities:
            for product in city.products:
                self.cities_per_product[product.value].append(
                    self.coordinate_to_index(city.coordinate))

    def _get_minimal_roads(self, product_index: int, current_cost: int, set_of_cities: typing.Set):
        if product_index == len(Product):
            if self.best_answer is None or current_cost < self.best_cost:
                self.best_cost = current_cost
                self.best_answer = copy.deepcopy(set_of_cities)
            return

        #for all cities that contain this product (with this index)
        for city_with_product_graph_idx in self.cities_per_product[product_index]:
            city_already_in_set = city_with_product_graph_idx in set_of_cities
            skip = False
            if not city_already_in_set:
                set_of_cities.add(city_with_product_graph_idx)
                updated_cost = current_cost + int(self.costs[self.source_city_idx_within_cities][city_with_product_graph_idx])
                if updated_cost > self.best_cost and self.best_answer is not None:
                    # There no reason to continue the current cost is already bad enough,
                    # so no point in continuing down this path
                    skip = True
            else:
                # We didn't add a city (it was already there), so cost hasn't changed
                updated_cost = current_cost

            if not skip:
                # Continue to the next product
                self._get_minimal_roads(product_index + 1, updated_cost, set_of_cities)

            # Backtracking - restore state - In any circumstance (skip/not skip)
            if not city_already_in_set:
                # We only remove a city if it was added at this iteration
                set_of_cities.remove(city_with_product_graph_idx)

    def get_roads_for_city(self, origin_city: City) -> str:
        paths_to_required_products = []
        origin_city_index = self.coordinate_to_index(origin_city.coordinate)
        self.source_city_idx_within_cities = self.get_index_in_city_indices(origin_city_index)

        #These two must be re-set here (each time we call get_roads_for_city)
        self.best_answer = None
        self.best_cost = sys.maxsize  # int

        self._get_minimal_roads(0, 0, set())
        for dest_city_index in self.best_answer:
            if dest_city_index != origin_city_index:
                paths_to_required_products.append(", ".join(
                    str(self.index_to_coordinate(p)) for p in self.get_path(origin_city_index, dest_city_index)))

        return str(self.best_cost)+"\n"+ "\n".join(paths_to_required_products)
        # return "\n".join(paths_to_required_products)

