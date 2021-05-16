class Tree:

    def __init__(self, inOrderTrav: [int]):
        self.__treeName = "tree"
        self.__root = None
        self.__curr = None
        self.__inOrder = inOrderTrav
        self.build_tree()

    def build_tree(self):
        for idx, value in enumerate(self.__inOrder):
            self.__root = self.insert(self.__root, value, None, idx)

    def insert(self, root, value, parent, index):

        if root is None:
            return Node(value, parent, index)

        elif root.value <= value:
            root.right = self.insert(root.right, value, root, index)
        else:
            root.left = self.insert(root.left, value, root, index)

        return root

    def depth(self):
        return self.get_depth(self.__root, 0)

    def get_depth(self, node, level):
        if node is None:
            return level
        else:
            return max(self.get_depth(node.left, level + 1), self.get_depth(node.right, level + 1))

    def to_string(self):
        for i in range(self.depth()):
            self.to_string_recur(self.__root, i, 0)
            print()

    def to_string_recur(self, node, height, level):
        if node is None:
            print("   ", end="")
        elif level == height:
            print(node.value, "   ", end="")
        else:
            self.to_string_recur(node.left, height, level + 1)
            self.to_string_recur(node.right, height, level + 1)

    def pop(self):
        root = self.__root.value
        right = self.__root.right
        left = self.__root.left

        if self.__root.right is None:
            self.__root = self.largest(self.__root.left)
        else:
            self.__root = self.smallest(self.__root.right)

        self.__root.left = left
        self.__root.left.parent = self.__root
        self.__root.right = right
        self.__root.right.parent = self.__root

        if self.__root.parent.left.value == self.__root.value:
            self.__root.parent.left = None
        else:
            self.__root.parent.right = None

        self.__root.parent = None
        return root

    def smallest(self, node):
        if node is None or node.left is None:
            return node
        else:
            return self.smallest(node.left)

    def largest(self, node):
        if node is None or node.right is None:
            return node
        else:
            return self.smallest(node.right)

    # Finds the path from root node to given root of the tree.
    # Stores the path in a list path[], returns true if path
    # exists otherwise false




class Node:
    def __init__(self, value: int, parent, index):
        self.index = index
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None

    def __str__(self):
        if self.parent is None:
            return "{} [{}]".format(self.value, "None")
        else:
            return "{} [{}]".format(self.value, self.parent.value)

def findPath(root, path, i):
    # Baes Case
    if root is None:
        return False

    # Store this node is path vector. The node will be
    # removed if not in path from root to k
    path.append(root.index)

    # See if the k is same as root's key
    if root.index == i:
        return True

    # Check if k is found in left or right sub-tree
    if ((root.left != None and findPath(root.left, path, i)) or
            (root.right != None and findPath(root.right, path, i))):
        return True

        # If not present in subtree rooted with root, remove
    # root from path and return False

    path.pop()
    return False

    # Returns LCA if node n1 , n2 are present in the given
    # binary tre otherwise return -1

def findLCA(self, root, n1, n2):
    # To store paths to n1 and n2 fromthe root
    path1 = []
    path2 = []

    # Find paths from root to n1 and root to n2.
    # If either n1 or n2 is not present , return -1
    if (not findPath(root, path1, n1) or not findPath(root, path2, n2)):
        return -1

        # Compare the paths to get the first different value
    i = 0
    while (i < len(path1) and i < len(path2)):
        if path1[i] != path2[i]:
            break
        i += 1
    return path1[i - 1]


with open('tree.txt', 'r') as t, open('pairs.txt', 'r') as p:
    tree = t.read().rstrip()
    pairs = eval(p.read().rstrip())

my_tree = Tree(tree)
# print(my_tree.pop(), ": popped")
answer = []
m = len(pairs)
for i in range(m):
    u, v = pairs[i]
    answer.append(my_tree.findLCA(my_tree[0],u, v))
# print(my_tree.to_string())
# print(my_tree.lca(30, 80))

print(answer)
