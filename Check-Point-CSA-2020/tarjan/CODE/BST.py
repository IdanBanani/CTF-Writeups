class Node:
    def __init__(self, data):
        self.value = data
        self.left = None
        self.right = None


class BST:
    def __init__(self, root):
        self.root = root

    def in_order(self, start, traversal):
        if start:
            traversal = self.in_order(start.left, traversal)
            traversal.append(start.value)
            traversal = self.in_order(start.right, traversal)
        return traversal


def arr_to_tree(arr, root, i, n):
    if i < n:
        temp = Node(arr[i])
        root = temp
        root.left = arr_to_tree(arr, root.left, 2*i+1, n)
        root.right = arr_to_tree(arr, root.left, 2*i+2, n)
    return root


def main():
    # li = [9, 2, 7, 4, 0, 6, 8, 8, 2, 3]
    with open('tree.txt') as f:
        li = list(f.read())

    root = None
    root = arr_to_tree(li, root, 0, len(li))

    bst = BST(root)
    print(build(bst.in_order(root, [])))


if __name__ == '__main__':
    main()
