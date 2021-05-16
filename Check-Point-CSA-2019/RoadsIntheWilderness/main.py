from typing import Callable

import argparse
import time

from HexagonMap import HexagonMap

#TODO: add  conditiional imports according to user input?
# from RoadOptimizer1 import RoadOptimizerV1
from RoadOptimizerV2 import RoadOptimizerV2
from shared_structs import Terrain

# DEFAULT_INPUT_FILE = 'example.txt'
DEFAULT_INPUT_FILE = 'input_map.txt'
SOLVER = RoadOptimizerV2


def solve(hm: HexagonMap, output_file: str, solver: Callable):
    with open(output_file, "w") as o:
        # ro = RoadOptimizerV1(hm)
        ro = solver(hm)
        print("Calculated initial costs in {} seconds".format(time.time() - start))
        for i, city in enumerate(hm.cities):
            # For debug purposes, print the current city index we are writing now
            print("City {}/{}".format(i + 1, len(hm.cities)), end="\r")
            print()
            # Writing the output to the file the server expects
            print(ro.get_roads_for_city(city), file=o)


#####################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file',
                        help='Input file name', default=DEFAULT_INPUT_FILE)
    parser.add_argument('-o', '--output_file',
                        help='Output file name')

    args = parser.parse_args()

    hm = HexagonMap({Terrain.OPEN: 1, Terrain.WOOD: 2, Terrain.MOUNTAIN: 6,
                     Terrain.DESERT: 7, Terrain.SWAMP: 4})

    output_file = args.output_file if args.output_file else "out_" + args.input_file

    start = time.time()
    hm.from_data_file(args.input_file)
    solve(hm, output_file, SOLVER)
    end = time.time()
    print("Parsed {} cities, Done in {} seconds".format(len(hm.cities), end - start))
