import networkx as nx

from collections import defaultdict
from collections.abc import Mapping, Set
from itertools import chain, count
from networkx.utils import arbitrary_element, UnionFind, generate_unique_node

"""
Lowest common ancestor (lca) for a given pair of nodes.
"""


def tarjan(G, root=None, pairs=None):
    """
    LCA for graph G with Tarjan's algorithm tarjan.
    """
    if len(G) == 0:
        raise nx.NetworkXPointlessConcept("LCA meaningless on null graphs.")
    elif None in G:
        raise nx.NetworkXError("None is not a valid node.")
    # Index pairs of interest for efficient lookup from either side.
    if pairs is not None:
        pair_dict = defaultdict(set)
        # See note on all_pairs_lowest_common_ancestor.
        if not isinstance(pairs, (Mapping, Set)):
            pairs = set(pairs)
        for u, v in pairs:
            for n in (u, v):
                if n not in G:
                    msg = "The node %s is not in the digraph." % str(n)
                    raise nx.NodeNotFound(msg)
            pair_dict[u].add(v)
            pair_dict[v].add(u)
    if root is None:
        for n, deg in G.in_degree:
            if deg == 0:
                if root is not None:
                    msg = "No root specified and tree has multiple sources."
                    raise nx.NetworkXError(msg)
                root = n
            elif deg > 1:
                msg = "Tree LCA only defined on trees; use DAG routine."
                raise nx.NetworkXError(msg)
    if root is None:
        raise nx.NetworkXError("Graph contains a cycle.")
    uf = UnionFind()
    ancestors = {}
    for node in G:
        ancestors[node] = uf[node]
    colors = defaultdict(bool)
    for node in nx.dfs_postorder_nodes(G, root):
        colors[node] = True
        for v in (pair_dict[node] if pairs is not None else G):
            if colors[v]:
                # If the user requested both directions of a pair, give it.
                # Otherwise, just give one.
                if pairs is not None and (node, v) in pairs:
                    yield (node, v), ancestors[uf[v]]
                if pairs is None or (v, node) in pairs:
                    yield (v, node), ancestors[uf[v]]
        if node != root:


def allpairslca(G, pairs=None):
    """
    Compute the lowest common ancestor for pairs of nodes.
    """
    if not nx.is_directed_acyclic_graph(G):
        raise nx.NetworkXError("LCA only defined on directed acyclic graphs.")
    elif len(G) == 0:
        raise nx.NetworkXPointlessConcept("LCA meaningless on null graphs.")
    elif None in G:
        raise nx.NetworkXError("None is not a valid node.")
    if (not isinstance(pairs, (Mapping, Set)) and pairs is not None):
        pairs = set(pairs)
    sources = [n for n, deg in G.in_degree if deg == 0]
    if len(sources) == 1:
        root = sources[0]
        super_root = None
    else:
        G = G.copy()
        super_root = root = generate_unique_node()
        for source in sources:
            G.add_edge(root, source)
    spanning_tree = nx.dfs_tree(G, root)
    dag = nx.DiGraph((u, v) for u, v in G.edges
                     if u not in spanning_tree or v not in spanning_tree[u])
    spanning_tree.add_nodes_from(G)
    dag.add_nodes_from(G)
    counter = count()
    root_distance = {root: next(counter)}
    for edge in nx.bfs_edges(spanning_tree, root):
        for node in edge:
            if node not in root_distance:
                root_distance[node] = next(counter)
    euler_tour_pos = {}
    for node in nx.depth_first_search.dfs_preorder_nodes(G, root):
        if node not in euler_tour_pos:
            euler_tour_pos[node] = next(counter)
    pairset = set()
    if pairs is not None:
        pairset = set(chain.from_iterable(pairs))
    for n in pairset:
        if n not in G:
            msg = "The node %s is not in the digraph." % str(n)
            raise nx.NodeNotFound(msg)
    ancestors = {}
    for v in dag:
        if pairs is None or v in pairset:
            my_ancestors = nx.dag.ancestors(dag, v)
            my_ancestors.add(v)
            ancestors[v] = sorted(my_ancestors, key=euler_tour_pos.get)

    def computedag(tree_lca, dry_run):
        """
        Iterate through the in-order merge for each pair of interest.
        We do this to answer the user's query, but it is also used to
        avoid generating unnecessary tree entries when the user only
        needs some pairs.
        """
        for (node1, node2) in pairs if pairs is not None else tree_lca:
            best_root_distance = None
            best = None
            indices = [0, 0]
            ancestors_by_index = [ancestors[node1], ancestors[node2]]

            def getnext(indices):
                """
                Returns index of the list containing the next item
                Next order refers to the merged order.
                Index can be 0 or 1 (or None if exhausted).
                """
                index1, index2 = indices
                if (index1 >= len(ancestors[node1]) and
                        index2 >= len(ancestors[node2])):
                    return None
                elif index1 >= len(ancestors[node1]):
                    return 1
                elif index2 >= len(ancestors[node2]):
                    return 0
                elif (euler_tour_pos[ancestors[node1][index1]] <
                      euler_tour_pos[ancestors[node2][index2]]):
                    return 0
                else:
                    return 1
            i = get_next_in_merged_lists(indices)
            cur = ancestors_by_index[i][indices[i]], i
            while i is not None:
                prev = cur
                indices[i] += 1
                i = get_next_in_merged_lists(indices)
                if i is not None:
                    cur = ancestors_by_index[i][indices[i]], i
                    # Two adjacent entries must not be from the same list
                    # in order for their tree LCA to be considered.
                    if cur[1] != prev[1]:
                        tree_node1, tree_node2 = prev[0], cur[0]
                        if (tree_node1, tree_node2) in tree_lca:
                            ans = tree_lca[tree_node1, tree_node2]
                        else:
                            ans = tree_lca[tree_node2, tree_node1]
                        if not dry_run and (best is None or root_distance[ans] > best_root_distance):
                            best_root_distance = root_distance[ans]
                            best = ans
            # If the LCA is super_root, there is no LCA in the user's graph.
            if not dry_run and (super_root is None or best != super_root):
                yield (node1, node2), best
    if pairs is None:
        # We want all pairs so we'll need the entire tree.
        tree_lca = dict(tarjan(spanning_tree, root))
    else:
        # We only need the merged adjacent pairs by seeing which queries the
        # algorithm needs then generating them in a single pass.
        tree_lca = defaultdict(int)
        for _ in computedag(tree_lca, True):
            pass
        # Replace the bogus default tree values with the real ones.
        for (pair, lca) in tarjan(spanning_tree, root, tree_lca):
            tree_lca[pair] = lca
    return computedag(tree_lca, False)


def lca(G, node1, node2, default=None):
    """
    Compute the lowest common ancestor of the given pair of nodes.
    Only defined on non-null directed acyclic graphs.
    Takes n log(n) time in the size of the graph.
    """
    ans = list(allpairslca(G, pairs=[(node1, node2)]))
    if ans:
        assert len(ans) == 1
        return ans[0][1]
    else:
        return default
