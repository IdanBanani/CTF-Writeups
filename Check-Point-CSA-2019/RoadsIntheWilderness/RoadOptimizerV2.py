import sys
from collections import defaultdict, namedtuple

import typing

from HexagonMap import HexagonMap
from OptimizerBase import RoadOptimizerBase
from shared_structs import Product, City


class RoadOptimizerV2(RoadOptimizerBase):
    MAX_VAL = sys.maxsize

    def __init__(self, hm: HexagonMap):
        super().__init__(hm)

        # Mapping of each city to the set of products it holds
        self.cities_to_products = defaultdict(set)
        for city in hm.cities:
            for product in city.products:
                self.cities_to_products[self.coordinate_to_index(city.coordinate)].add(product)

        # The set of all products
        self.all_products = set((p for p in Product))



    @classmethod
    def partition(cls, collection: typing.Collection) -> typing.List:
        """
        Generate all different partitions of a given collection.
        A partition of a set is a grouping of the set's elements into non-empty subsets,
        in such a way that every element is included in exactly one subset.
        """
        if len(collection) == 1:
            yield [collection]
            return

        first = collection[0]
        for smaller in cls.partition(collection[1:]):
            # Insert 'first' in each of the subpartitions' subsets
            for n, subset in enumerate(smaller):
                yield smaller[:n] + [[first] + subset] + smaller[n + 1:]
            # Put 'first' in its own subset
            yield [[first]] + smaller

    def get_roads_for_city(self, origin_city: City) -> str:
        Pair = namedtuple('Pair', 'cost city_index')
        paths = []

        # The list of products which the origin city does NOT have.
        missing_products = list(
            self.all_products - self.cities_to_products[self.coordinate_to_index(origin_city.coordinate)])

        origin_city_index = self.coordinate_to_index(origin_city.coordinate)
        origin_index_in_city_indices = self.get_index_in_city_indices(origin_city_index)

        candidates = []
        for partition in self.partition(missing_products):
            # For every way to partition the missing product list:
            lst = []
            for subset in partition:
                # For each subset of the current way to partition the missing products:
                min_cost = self.MAX_VAL
                min_city = None
                for dest_city_index in self.cities_to_products:
                    if set(subset).issubset(self.cities_to_products[dest_city_index]) and self.costs[
                        origin_index_in_city_indices, dest_city_index] < min_cost:
                        # If the current destination city has all the products in the current subset, and the cost to the destination
                        # city is lower than the previous minimum, save the current result as the new minimum
                        min_cost, min_city = int(
                            self.costs[origin_index_in_city_indices, dest_city_index]), dest_city_index

                if min_cost == self.MAX_VAL:
                    # We couldn't find any city with all the missing products of the current subset
                    break

                lst.append(Pair(min_cost, min_city))

            #Check why the for loop ended (for subset in partition)
            if len(lst) == len(partition):
                # For the current partition of missing products, we were able to find for each subset the minimal-cost city
                # which has all the resources of the subset.
                partition_cost = sum((pair.cost for pair in lst))
                candidates.append(Pair(partition_cost, [pair.city_index for pair in lst]))

        # Find the solution with the minimal cost among all solution candidates
        total_cost, cities = min(candidates, key=lambda x: x.cost)

        for dest_city_index in cities:
            lst = ", ".join(str(self.index_to_coordinate(p)) for p in self.get_path(origin_city_index, dest_city_index))
            paths.append(lst)

        return "\n".join(paths)
        # return str(total_cost) + "\n" + "\n".join(paths)
