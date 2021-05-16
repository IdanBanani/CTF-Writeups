# TODO: The code works (for data.py input), but gets halt (doesn't end/returns)
from dataclasses import dataclass, field
from typing import Any
import queue as Q
import networkx as nx
import itertools as it

#TODO: Here he stores the "modified" input file
from Sol3.data import *

# TODO: The example input fails the program
#    G.add_edge(tupToNode((lastx, lasty)), tupToNode((i, j)), weight=weights[mmaped_input[i][j]])
# IndexError: list index out of range
# Too bad we are not given the code which did the modification to the original input
# (This solution depends on that parsing method)
# from Sol3.data_test import *

N = 64
Rw = N * N + 1
Rs = N * N + 2
Rp = N * N + 3
Rt = N * N + 4
Rc = N * N + 5
Ro = N * N + 6
Rall = [Rw, Rs, Rp, Rt, Rc, Ro]
Rcomb = {}
Rcomb_idx = Ro + 1

C = 99999
all_res = ["s", "p", "t", "w", "c", "o"]
all_terrains = {"m": 6, "w": 2, "o": 1, "s": 4, "d": 7}
outp = open("out.txt", "w")
weights = {'o': 1, 'w': 2, 's': 4, 'm': 6, 'd': 7}  # dict of edges and their weight

comb_dict = {}  # key: city. val: (dict: key: resource combination. val: (cost, path to resource)


def tupToNode(t):
    return t[1] * N + t[0]


def nodeToTup(n):
    return ((n % N), int(n / N))


class point:
    def __init__(self, x, y, d, p, r=None):
        self.x = x
        self.y = y
        self.node = x * N + y
        self.res = r
        self.comb_dist = {}
        self.dist_from_city = (d, p)

    def addResPath(self, r, p, d):
        self.comb_dist[r] = (p, d)


G = nx.DiGraph()
for i in range(N):
    for j in range(N):
        G.add_node(i * N + j)
G.add_nodes_from(Rall)


def unique_group(iterable, k, n):
    """Return an iterator, comprising groups of size `k` with combinations of size `n`."""
    # Build separate combinations of `n` characters
    groups = ("".join(i) for i in it.combinations(iterable, n))  # 'AB', 'AC', 'AD', ...

    # Build unique groups of `k` by keeping the longest sets of characters
    return (i for i in it.combinations(groups, k)
            if len(set("".join(i))) == sum((map(len, i))))  # ('AB', 'CD'), ('AB', 'CE'), ...


def combined(groups1, groups2):
    """Return an iterator with unique combinations of groups (k and l)."""
    # Build a unique cartesian product of groups `k` and `l`, filtering non-disjoints
    return (i[0] + i[1]
            for i in it.product(groups1, groups2)
            if set("".join(i[0])).isdisjoint(set("".join(i[-1]))))


iterable = "sptwco"
g1 = unique_group(iterable, 1, 6)
fixed_combs = list((g1))

g2 = unique_group(iterable, 1, 5)
g3 = unique_group(iterable, 1, 1)

fixed_combs += list(combined(g2, g3))

g4 = unique_group(iterable, 1, 4)
g5 = unique_group(iterable, 1, 2)

fixed_combs += list(combined(g4, g5))

g6 = unique_group(iterable, 1, 4)
g7 = unique_group(iterable, 2, 1)

fixed_combs += list(combined(g6, g7))

g8 = unique_group(iterable, 2, 3)

fixed_combs += list((g8))

g9 = unique_group(iterable, 1, 3)
g10 = unique_group(iterable, 1, 2)
g11 = unique_group(iterable, 1, 1)

fixed_combs += list(combined(combined(g9, g10), g11))

g20 = unique_group(iterable, 1, 3)
g21 = unique_group(iterable, 3, 1)

fixed_combs += list(combined(g20, g21))

g12 = unique_group(iterable, 3, 2)

fixed_combs += list((g12))

g13 = unique_group(iterable, 2, 2)
g14 = unique_group(iterable, 2, 1)

fixed_combs += list(combined(g13, g14))

g15 = unique_group(iterable, 1, 2)
g16 = unique_group(iterable, 4, 1)

fixed_combs += list(combined(g15, g16))

g17 = unique_group(iterable, 6, 1)

fixed_combs += list((g17))

print(len(fixed_combs))

# add edges to neighbours
for lastx in range(N):
    for lasty in range(N):
        for i in range(lastx - 1, lastx + 2):
            for j in range(lasty - 1, lasty + 2):
                if i == lastx and j == lasty:
                    continue
                if i >= N or i < 0 or j >= N or j < 0:
                    continue
                if lastx % 2 == 0 and ((i == lastx - 1 and j == lasty + 1) or (i == lastx + 1 and j == lasty + 1)):
                    continue
                elif lastx % 2 != 0 and ((i == lastx + 1 and j == lasty - 1) or (i == lastx - 1 and j == lasty - 1)):
                    continue
                G.add_edge(tupToNode((lastx, lasty)), tupToNode((i, j)), weight=weights[mmaped_input[i][j]])

# add edges from R_ (fake node) to cities with the resource
res_dict = {}
for c in cities.keys():
    x, y = c[0], c[1]
    node = tupToNode((x, y))
    for r in cities[(x, y)]:
        if r == "s":
            G.add_edge(Rs, node, weight=weights[mmaped_input[x][y]])
            res_dict[Rs] = "s"
        elif r == "o":
            G.add_edge(Ro, node, weight=weights[mmaped_input[x][y]])
            res_dict[Ro] = "o"
        elif r == "t":
            G.add_edge(Rt, node, weight=weights[mmaped_input[x][y]])
            res_dict[Rt] = "t"
        elif r == "w":
            G.add_edge(Rw, node, weight=weights[mmaped_input[x][y]])
            res_dict[Rw] = "w"
        elif r == "p":
            G.add_edge(Rp, node, weight=weights[mmaped_input[x][y]])
            res_dict[Rp] = "p"
        else:
            G.add_edge(Rc, node, weight=weights[mmaped_input[x][y]])
            res_dict[Rc] = "c"


def listToStr(l):
    out = ""
    for i in l:
        out += i
    return out


# add combinations resources to the graph
res = [it.combinations(all_res, i) for i in range(2, 7)]
res = [list(c) for c in
       res]  # each element in the list is a list of tuples containing resources. ex: index 0 has a list of tuples size 2, 1 has of size 3 etc...
for l in res:
    for i in range(len(l)):
        l[i] = listToStr(sorted(l[i]))

for rg in res:
    for r in rg:
        G.add_node(Rcomb_idx)
        Rcomb[Rcomb_idx] = r
        Rcomb[r] = Rcomb_idx
        Rcomb_idx += 1
for c in cities.keys():
    group_len = 2
    for rgroup in res:
        for r in rgroup:  # ex: r = ('w', 'o', 's')
            lr = [x for x in r]
            if set(lr).issubset(set(cities[c])):
                G.add_edge(Rcomb[r], tupToNode(c), weight=weights[mmaped_input[c[0]][c[1]]])
        group_len += 1

# get path from each resource to every point on the map
city_path = {}
opt = {}
for c in cities.keys():
    city_path[c] = {}
    opt[c] = {}
for r in Rall:
    pred, dist = nx.dijkstra_predecessor_and_distance(G, r, cutoff=None, weight='weight')
    r_str = res_dict[r]
    for c in cities.keys():
        node = tupToNode((c[0], c[1]))
        path_to_add = [c]
        # city_path[c][r_str] = [c]
        opt[c][r_str] = pred.copy()
        if len(pred[node]) == 0:  # city has resource
            city_path[c][r_str] = (0, [c])
            continue
        curr = pred[node][0]  # multi choice
        curr_tup = nodeToTup(curr)  # (int(curr/N), (curr%N))
        path_dist = dist[node] - weights[mmaped_input[c[0]][c[1]]]
        while curr != r:
            # city_path[c][r_str] += [curr_tup]
            path_to_add += [curr_tup]
            curr = pred[curr][0]  # multiple choices
            curr_tup = nodeToTup(curr)  # (int(curr/N), (curr%N))
        city_path[c][r_str] = (path_dist, path_to_add.copy())

for rg in res:
    for r in rg:
        pred, dist = nx.dijkstra_predecessor_and_distance(G, Rcomb[r], cutoff=None, weight='weight')
        for c in cities.keys():
            node = tupToNode((c[0], c[1]))
            path_to_add = [c]
            # city_path[c][r] = [c]
            opt[c][r] = pred.copy()
            if node not in pred.keys():  # no city with this resource combination
                city_path[c][r] = (-1, [])
                continue
            if len(pred[node]) == 0:  # city has resource
                city_path[c][r] = (0, [c])
                continue
            path_cost = dist[node] - weights[mmaped_input[c[0]][c[1]]]
            curr = pred[node][0]  # multi choice
            curr_tup = nodeToTup(curr)  # (int(curr/N), (curr%N))
            while curr != Rcomb[r]:
                # city_path[c][r] += [curr_tup]
                path_to_add += [curr_tup]
                curr = pred[curr][0]  # multiple choices
                curr_tup = nodeToTup(curr)  # (int(curr/N), (curr%N))
            city_path[c][r] = (path_cost, path_to_add.copy())

min_cover, min_cover_paths = C, []


def resourceStrToTup(s):
    s = sorted([x for x in s])
    t = (s[0],)
    for i in range(1, len(s)):
        t += (s[i],)
    return t


def minCombCover2(c):
    global min_cover, min_cover_paths
    for comb in fixed_combs:  # comb: ('sptwo', 'c') for example
        unreach = False
        sum = 0
        curr_path = []
        for n in comb:  # n: 'sptwo'
            n = ''.join(sorted([i for i in n]))
            res_cost_path = (city_path[c][n])
            if res_cost_path[0] == -1:
                unreach = True
                break
            sum += res_cost_path[0]
            curr_path += [res_cost_path[1]]
        if unreach:
            continue
        if sum < min_cover:
            min_cover = sum
            min_cover_paths = curr_path


# find best combination for every city:
for c in cities.keys():
    print("Working on city: " + str(c))
    left_res = [r for r in all_res if r not in cities[c]]
    city_combs = [(k, city_path[c][k]) for k in city_path[c].keys() if len((city_path[c][k])[1]) != 0]
    minCombCover2(c)
    for p in min_cover_paths:
        if len(p) <= 1:
            continue
        for t in p:
            outp.write(str(t) + ", ")
        outp.write("!\n")
    min_cover, min_cover_paths = C, []
    # print(city_combs)
outp.close()
