from binarytree import build

# Build a tree from list representation
with open('tree.txt') as f:

    dirty = f.read()

values = dirty
root = build(values)
print(root)
#
#            __7
#           /   \
#        __3     2
#       /   \     \
#      6     9     1
#     / \
#    5   8
#
# >> >  # Convert the tree back to list representation
# >> > root.values
# [7, 3, 2, 6, 9, None, 1, 5, 8]
