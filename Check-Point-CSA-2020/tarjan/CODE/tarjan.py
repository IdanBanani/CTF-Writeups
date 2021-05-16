import networkx as nx

tree = None
with open('tree.txt', 'r') as t, open('pairs.txt', 'r') as p:
    tree = t.read().rstrip()
    pairs = eval(p.read().rstrip())

pairs_set = set()
for pair in pairs:
    u, v = pair
    pairs_set.add(tuple((tree[u], tree[v])))

G = nx.DiGraph()
G.add_nodes_from(tree)
for i in range(len(tree)//2):
    G.add_edge(tree[i], tree[2*i + 1])

    if (2*i + 2) < len(tree):
        G.add_edge(tree[i], tree[2*i + 2])

answer = nx.algorithms.lowest_common_ancestors.tree_all_pairs_lowest_common_ancestor(
    G, root=tree[0], pairs=pairs_set)
print(list(answer))
