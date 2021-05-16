import numpy as np


class FullBinaryTree(object):

    '''Implements a full binary tree; each nodes should have exactly two children,
       left and right, and one parent. For interal nodess left and right are
       are other internal nodess. For leaves, the are both None. All nodess
       have a parent that is an internal nodes except the root whose parent
       is None. Tree must contain at least one nodes.'''

    def __init__(self, value, left=None, right=None, parent=None):
        '''Constructor creates a single nodes tree as default. Sets
           parent relation if left and right are given.'''
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

        if self.left:
            self.left.set_parent(self)
        if self.right:
            self.right.set_parent(self)

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def set_parent(self, tree):
        '''Sets a given tree as a parent nodes'''
        self.parent = tree

    def get_parent(self):
        '''Returns a parent nodes'''
        return self.parent

    def get_value(self):
        return self.value

    def is_leaf(self):
        '''Returns true iff nodes is a leaf'''

        return not self.left and not self.right

    def is_root(self):
        '''Returns true iff nodes is the root'''

        return not self.parent

    def size(self):
        '''Returns the size of the tree'''

        if self.is_leaf():
            return 1
        else:
            return 1 + self.left.size() + self.right.size()

    def height(self):
        '''Returns the height of the tree'''

        if self.is_leaf():
            return 0
        else:
            return 1 + max((self.left.height(), self.right.height()))

    def lca(self, tree):
        '''Returns the least common answer of self and tree'''

        my_anc = self.list_of_ancestors()
        tree_anc = tree.list_of_ancestors()
        i = 0
        while i < len(my_anc) and i < len(tree_anc) and my_anc[i] == tree_anc[i]:
            i = i+1
        if my_anc[i-1] == tree_anc[i-1]:
            return my_anc[i-1]
        else:
            return None

    def contains(self, tree):
        '''Returns true iff self contains tree as a subtree'''

        if self == tree:
            return True
        elif self.is_leaf():
            return False
        else:
            return self.left.contains(tree) or self.right.contains(tree)

    def list_of_ancestors(self):
        '''Returns list of ancestors including self'''

        if self.is_root():
            return [self]
        else:
            return self.parent.list_of_ancestors() + [self]

    def list_of_leaves(self):
        '''Returns a list of all of the leaves of tree'''

        if self.is_leaf():
            return [self]
        else:
            return self.left.list_of_leaves()+self.right.list_of_leaves()


with open('tree.txt', 'r') as t, open('pairs.txt', 'r') as p:
    tree = t.read().rstrip()
    pairs = eval(p.read().rstrip())


n = len(tree)
nodes = np.zeros((1, n), dtype=FullBinaryTree)
print(nodes.size)
print(nodes.shape)
for i in range(n//2):
    nodes[0, i] = FullBinaryTree(tree[i])

    if 2*i + 2 < n:
        nodes[0, 2*i + 2] = FullBinaryTree(tree[i], parent=nodes[0, i])
        nodes[0, i].set_right(nodes[0, 2*i + 2])

    if 2*i + 1 < n:
        nodes[0, 2*i + 1] = FullBinaryTree(tree[i], parent=nodes[0, i])
        nodes[0, i].set_left(nodes[0, 2*i + 1])


m = len(pairs)
answer = np.zeros((1, m))

pairs_set = set()
for i in range(m):
    u, v = pairs[i]

    pair_lca = nodes[0, u].lca(nodes[0, v])

    answer[0, i] = nodes[0, u].lca(nodes[0, v]).value if pair_lca else None

# for element in answer:
#   element.value
print(answer)
