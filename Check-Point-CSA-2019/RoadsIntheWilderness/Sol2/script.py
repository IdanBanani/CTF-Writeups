# import requests
#TODO: IdanB: I don't think this solution has ever worked
#TODO: It fails on parsing the input file, can you spot the mistake?
#      and it also parses it in a cryptic way

REMOVE_DUPLICATES_AND_REVERSED = True
REMOVE_OVERLAPPING = True
WRITE_TO_FILE = True
MAX_INT = 1 << 31 - 1
RESOURCES_LIST = ['produce', 'wood', 'stone', 'clay', 'ore', 'textile']
MY_INPUT = "input_test.txt"
# MY_INPUT = "input_test_old.txt"


# To be used as paths tree
class TreeNodeNonBinary:
    def __init__(self, val=0):
        self.parent = 0
        self.val = val
        self.children = []

    def AddSon(self, val):
        node = TreeNodeNonBinary(val)
        self.children.append(node)
        node.parent = self
        return node

    def RemoveSon(self, son_val):
        if son_val in self.children:
            self.children.remove(son_val)
        else:
            return -1
        return 0


class TerrainType:
    def __init__(self, type_str):
        self.name = type_str
        self.cost = self.TypeToCost(type_str)

    def TypeToCost(self, type_str):
        terrain_map = {'mountain': 6, 'wood': 2, 'open': 1, 'swamp': 4, 'desert': 7}
        if type_str.lower().replace(' ', '') in terrain_map:
            return terrain_map[type_str]
        else:
            raise Exception("Invalid terrain type {}".format(type_str))

    def GetCost(self):
        return self.cost

    def GetName(self):
        return self.name


class Coordinate:
    def __init__(self, coordinate, city, terrain_type, board_size):
        self.coordinate = coordinate
        self.city = city
        self.terrain = TerrainType(terrain_type)
        self.neigh_coordinates_tup = self.GenNeighCoord(board_size)
        self.neigh_coordinates = []

    def GenNeighCoord(self, board_size):
        coord_x = self.coordinate[0]
        coord_y = self.coordinate[1]
        if coord_x % 2 == 0:
            full_list = [(coord_x + 1, coord_y), (coord_x - 1, coord_y), (coord_x - 1, coord_y - 1),
                         (coord_x + 1, coord_y - 1), (coord_x, coord_y - 1), (coord_x, coord_y + 1)]
        else:
            full_list = [(coord_x + 1, coord_y), (coord_x - 1, coord_y), (coord_x - 1, coord_y + 1),
                         (coord_x + 1, coord_y + 1), (coord_x, coord_y - 1), (coord_x, coord_y + 1)]
        final_list = []
        for neigh in full_list:
            if neigh[0] < 0 or neigh[0] >= board_size[0] or neigh[1] < 0 or neigh[1] >= board_size[1]:
                continue
            else:
                final_list.append(neigh)
        return final_list

    def __repr__(self):
        return str(self.coordinate)


class Path:
    def __init__(self, key, coordinates_list, tot_cost, additional_resources_on_path):
        self.path_key = key
        self.coordinates_list = coordinates_list
        if coordinates_list != 0:
            self.coordinates_only_repr = [x.coordinate for x in coordinates_list]
        else:
            self.coordinates_only_repr = 0
        self.tot_path_cost = tot_cost
        # deprecated
        self.additional_resources_on_path = additional_resources_on_path


class City:
    def __init__(self, city_name, city_coordinate, city_resources):
        self.name = city_name
        self.coordinate = city_coordinate
        self.resources = city_resources


class Map:
    def __init__(self, text_map_file):
        self.map, self.cities = self.ConvertTextToMap(text_map_file)

    def ConvertTextToMap(self, input_file):
        # One run to get dimensions
        input_list_lines = input_file.split('\n')
        num_rows = 0
        num_cols = 0
        city_num = 0
        for line in input_list_lines:
            if len(line) > 0:
                if line[0] == '[':
                    num_cols += 1
        # Second run to build map
        coordinates_dict = {}
        cities_list = []
        col_num = 0
        print("# Transforming input file to internal structure...")
        for line in input_list_lines:
            if len(line) > 0:
                if line[0] == '[':
                    stripped_col = line.replace('[', '').replace(']', '').replace(' ', '').replace('\n', '')
                    if stripped_col[-1] == ',':
                        stripped_col = stripped_col[:-1]
                    col_as_list = stripped_col.split(',')
                    if num_rows == 0:
                        num_rows = len(col_as_list)
                    row_num = 0
                    for row_terrain in col_as_list:
                        coordinates_dict[(col_num, row_num)] = Coordinate((col_num, row_num), 0, row_terrain,
                                                                          (num_cols, num_rows))
                        row_num += 1
                    col_num += 1
                # Assuming all coordinates were generated (the file starts with coordinates and then cities)
                elif line[0] == '(':
                    stripped_city = line.replace('(', '').replace(')', '').replace(' ', '').replace('\n', '')
                    city_att_list = stripped_city.split(',')
                    coordinate_inst = coordinates_dict[(int(city_att_list[0]), int(city_att_list[1]))]
                    curr_city = City(city_num, coordinate_inst, [res.lower() for res in city_att_list[2:]])
                    cities_list.append(curr_city)
                    coordinate_inst.city = curr_city
                    city_num += 1
        print("# Finished transforming input file to internal structure.")
        # Completing the missing list of references to neighboring coordinates in every coordinate
        print("# Generating neighbor coordinates references...")
        for coordinate in coordinates_dict:
            for neigh in coordinates_dict[coordinate].neigh_coordinates_tup:
                coordinates_dict[coordinate].neigh_coordinates.append(coordinates_dict[neigh])
        print("# Finished generating neighbor coordinates references.")
        return coordinates_dict, cities_list

    # Updates resources_dict with best path to get from city to each needed resource
    def FindBestPathsFromCity(self, city, resources_dict):
        # coordinates dictionary for ones we visited. conatines last best path. will be replaced each time we hit a coordinate with
        # a new cheaper path
        visited_coordinates_dict_from_city = {}
        # Initialize paths tree
        tree_from_city = TreeNodeNonBinary((city.coordinate, city.coordinate.terrain.GetCost()))
        # preparing the queue for the BFS search
        q_city = [tree_from_city]
        best_path_found = False
        while (not best_path_found):
            # Search from city, each iteration is an expanding level in the map (represented in new q_city).
            q_city, best_path_found = WalkOneLevelInGraphSearchRes(q_city, visited_coordinates_dict_from_city,
                                                                   resources_dict, city)


# Returns the list of coordinates from a given coordinate up the path and to the root (city)
def WalkTreeUpAndRetCoordinates(coordinate_node):
    curr_node = coordinate_node
    coordinates_list = []
    while curr_node != 0:
        coordinates_list.append(curr_node.val[0])
        curr_node = curr_node.parent
    return coordinates_list


# One iteration of the BFS algorithm. go over nodes in q. Add to visited or replace entry in visited if the node represents a
# better path to coordinate. Each time a city is met, for each of its resource the origin city needs, check if that's the best
# path to get to it so far and update resources_dict.
def WalkOneLevelInGraphSearchRes(q_city, visited_coordinates_dict_from_city, resources_dict, city):
    # This will stay True only when every path in the current q is more expensive than the existing paths found for resources.
    # In this case we terminate the search
    all_res_found_better_path = True
    # Find only the resources needed for the city
    needed_resources = list(set(RESOURCES_LIST) - set(city.resources))
    # initialize queue for next iteration of BFS
    q_to_q_city = []
    while q_city != []:
        # The represantion of the current coordinate as a node in paths tree
        curr_coordinate_node = q_city[0]
        # The representation as a Coordinate instance
        curr_coordinate_as_coordinate = curr_coordinate_node.val[0]
        # The cost of getting to the coordinate on this path
        curr_coordinate_path_cost = curr_coordinate_node.val[1]
        # If this is the first time we hit the coordinate
        if curr_coordinate_as_coordinate not in visited_coordinates_dict_from_city:
            # Update the dictionary
            visited_coordinates_dict_from_city[curr_coordinate_as_coordinate] = curr_coordinate_node
            # Any hope in this path? are there resources that it is currently more expensive to get to
            # than the current cost of the path?
            for res in resources_dict:
                if resources_dict[res].tot_path_cost >= curr_coordinate_path_cost:
                    all_res_found_better_path = False
            # If so, check if it has new resources and add neighbors to next layer of expansion (next BFS iteration)
            # If not, we don't want to continue on this path. no need to add neighbors to next iteration, no need to check resources.
            if not all_res_found_better_path:
                # Did we stumble upon a resource?
                if curr_coordinate_as_coordinate.city != 0:
                    intersect_needed_resources = [res for res in needed_resources if
                                                  res in curr_coordinate_as_coordinate.city.resources]
                    for res in intersect_needed_resources:
                        path_to_res = Path(CityResToKey(city, res), WalkTreeUpAndRetCoordinates(curr_coordinate_node),
                                           curr_coordinate_path_cost, 0)
                        if res in resources_dict:
                            # If there's already a path to the resource, choose the better one
                            if path_to_res.tot_path_cost <= resources_dict[res].tot_path_cost:
                                resources_dict[res] = path_to_res
                        else:
                            # If not, add this one.
                            resources_dict[res] = path_to_res
                # Add neighbors to next iteration
                for next_coordinate in curr_coordinate_as_coordinate.neigh_coordinates:
                    new_node = curr_coordinate_node.AddSon(
                        (next_coordinate, curr_coordinate_path_cost + next_coordinate.terrain.GetCost()))
                    if new_node not in q_to_q_city:
                        q_to_q_city.append(new_node)
        # If we entered this coordinate before, we should check whether this time the cost is cheaper.
        # If so, we'll take the other path's children, update them with the lower cost and move on.
        else:
            last_best_path_to_coordinate_node = visited_coordinates_dict_from_city[curr_coordinate_as_coordinate]
            last_best_path_to_coordinate_cost = visited_coordinates_dict_from_city[curr_coordinate_as_coordinate].val[1]
            if curr_coordinate_path_cost <= last_best_path_to_coordinate_cost:
                # Steal already walked paths
                if curr_coordinate_node != last_best_path_to_coordinate_node:
                    curr_coordinate_node.children = last_best_path_to_coordinate_node.children
                    last_best_path_to_coordinate_node.children = []
                # Any hope in this path?
                all_res_found_better_path = True
                for res in resources_dict:
                    if resources_dict[res].tot_path_cost >= curr_coordinate_path_cost:
                        all_res_found_better_path = False
                # If so, check if it has new resources and add neighbors to next layer of expansion.
                if not all_res_found_better_path:
                    # Did we stumble upon a resource? do the same as above
                    if curr_coordinate_as_coordinate.city != 0:
                        intersect_needed_resources = [res for res in needed_resources if
                                                      res in curr_coordinate_as_coordinate.city.resources]
                        for res in intersect_needed_resources:
                            path_to_res = Path(CityResToKey(city, res),
                                               WalkTreeUpAndRetCoordinates(curr_coordinate_node),
                                               curr_coordinate_path_cost, 0)
                            if res in resources_dict:
                                if path_to_res.tot_path_cost <= resources_dict[res].tot_path_cost:
                                    resources_dict[res] = path_to_res
                            else:
                                resources_dict[res] = path_to_res
                # Update children paths
                for child in curr_coordinate_node.children:
                    child.parent = curr_coordinate_node
                    child.val = (child.val[0], curr_coordinate_path_cost + child.val[0].terrain.GetCost())
                    if child not in q_to_q_city and child not in q_city:
                        # add to current queue and not next queue so we will go over all existing nodes in paths and only
                        # then move to the next iteration in the BFS
                        q_city.append(child)
                # Update the coordinate dict on new path
                visited_coordinates_dict_from_city[curr_coordinate_as_coordinate] = curr_coordinate_node
            else:
                # This path was beaten, no updates and it will not create children and add them to the queue
                pass
        # Done with current coordinate (path node), remove from queue 
        q_city.remove(curr_coordinate_node)
    return q_to_q_city, all_res_found_better_path


def CityResToKey(city, res):
    return (city, res)


# Optional (see REMOVE_OVERLAPPING), remove paths from city that are completely contained in longer paths from same city
def IsPath1ContainedInPath2(path1, path2):
    path1_list = list(path1.coordinates_only_repr)
    path1_list.reverse()
    path2_list = list(path2.coordinates_only_repr)
    path2_list.reverse()
    if len(path1_list) > len(path2_list):
        return False
    if path1_list[0] != path2_list[0]:
        raise Exception("something went wrong")
    count = 1
    for coordinate in path1_list[1:]:
        if path2_list[count] == coordinate:
            count += 1
        else:
            return False
    return True


# map_file = 'input_test.txt'

# map_url = 'http://3.122.27.254/map'
# map_file = requests.get(map_url).text

# Generate structured map from text
# TODO: Add reading input from text file
# my_map = Map(map_file)
my_map = Map(MY_INPUT)
final_paths_list = []
# Go over every city and find its best paths to every resource it needs
for city in my_map.cities:
    resources_dict = {}
    # Initialize "worst" paths to each resource
    needed_resources = list(set(RESOURCES_LIST) - set(city.resources))
    for res in needed_resources:
        resources_dict[res] = Path(0, 0, MAX_INT, 0)
    # Run the algorithm to find the best route to each needed resource
    my_map.FindBestPathsFromCity(city, resources_dict)
    print("# Finished calculating paths from city " + str(city.coordinate.coordinate) + ".")
    paths = list(resources_dict.values())
    paths_final = paths[:]
    # Optional (see IsPath1ContainedInPath2)
    if REMOVE_OVERLAPPING:
        for path1 in paths:
            for path2 in paths:
                if path1 != path2 and path1 in paths_final:
                    if IsPath1ContainedInPath2(path1, path2):
                        paths_final.remove(path1)
    # Add best paths from city to final list
    final_paths_list += paths_final
    final_paths_list = list(set(final_paths_list))

explicit_paths_list = []
already_printed_dict = {}
# Get explicit list of paths by coordinates, avoid duplicates
# Optional (see REMOVE_DUPLICATES_AND_REVERSED) - one more filter: remove duplicate paths and paths that appear twice from 2 end cities
for path in final_paths_list:
    if REMOVE_DUPLICATES_AND_REVERSED:
        if str(path.coordinates_only_repr) not in already_printed_dict and str(
                path.coordinates_only_repr[::-1]) not in already_printed_dict:
            already_printed_dict[str(path.coordinates_only_repr)] = True
            explicit_paths_list.append(path.coordinates_only_repr)
    else:
        explicit_paths_list.append(path.coordinates_only_repr)

# Optional (see WRITE_TO_FILE) - write output to file
if WRITE_TO_FILE:
    output_file = open('output.txt', 'w')
final_str = ''
for line in explicit_paths_list:
    # format according to instructions
    line_str = (str(line) + '\n').replace('[', '').replace(']', '')
    final_str += line_str
    if WRITE_TO_FILE:
        output_file.write(line_str)
# print(final_str)
if WRITE_TO_FILE:
    output_file.close()

# # Test
# server_url = 'http://3.122.27.254/solution'
# r = requests.post(server_url, data = final_str)
# print("Response from server: " + r.text)
