import re
import glob
import os
import hashlib

from abc import ABC


class MerkleObject(ABC):

    def __init__(self, hash_func):
        self.hash_func = hash_func

    def get_hash(self):
        raise NotImplementedError

    def get_height(self):
        raise NotImplementedError


class MerkleLeaf(MerkleObject):

    def __init__(self, hash_func, data):
        super().__init__(hash_func)
        hashed_data = hash_func(data)
        as_hexdigest = hashed_data.hexdigest()
        self.hash = as_hexdigest

    # @property
    def get_hash(self):
        return self.hash

    def get_height(self):
        return 0


class MerkleNode(MerkleObject):

    def __init__(self, hash_func, expected_num_children):
        # super().__init__(hash_func)
        self.hash_func = hash_func
        self.expected_num_children = expected_num_children
        self.children = []

    def add_child(self, child):
        if len(self.children) >= self.expected_num_children:
            raise ValueError('Error: Too many children added to current node'
                             )
        if not isinstance(child, MerkleObject):
            raise ValueError('Error: Expecting a MerkleObject')
        if self.hash_func != child.hash_func:
            raise ValueError('Error: Hash function mismatch')

        self.children.append(child)

    def get_num_children(self):
        return len(self.children)

    def get_hash(self):
        if len(self.children) != self.expected_num_children:
            raise RuntimeError('Error: Missing children')

        res = ''
        # for c in self.children:
        #     res += c.get_hash()
        res = ''.join([c.get_hash() for c in self.children])
        encoded = res.encode('ascii')
        hashed = self.hash_func(encoded)
        return hashed.hexdigest()

    def get_height(self):
        return self.children[0].get_height() + 1

#######################################################

################################################


def calculate_root(path, height, num_sons):
    queue = [] #temp queue , max size at any moment = H (heigt)

    file_id = 0 # Leaf file ID

    # num_of_non_leaf_nodes = (num_sons ** height) // num_sons
    num_of_leaf_parents = num_sons ** (height-1)

    for i in range(num_of_leaf_parents):
        n = MerkleNode(hashlib.md5, num_sons)
        for j in range(num_sons):
            with open(os.path.join(path, 'tx_{}'.format(file_id)), 'rb'
                      ) as f:
                n.add_child(MerkleLeaf(hashlib.md5, f.read()))

            file_id += 1
        queue.append(n)

    while len(queue) != 1:
        num_of_leaf_parents = num_of_leaf_parents // num_sons
        for i in range(num_of_leaf_parents):
            n = MerkleNode(hashlib.md5, num_sons)
            for j in range(num_sons):
                n.add_child(queue.pop(0))

            queue.append(n)

    assert queue[0].get_height() == height
    return queue[0] #return root


def generate_roots(subdir):
    roots = {}

    EXTRACT_HEIGHT_SONS_RE = \
        re.compile(r"block_(\d+)-height_(\d+)-sons_(\d+)$")

    for filename in glob.iglob(os.path.join(subdir, '*'),
                               recursive=False):
        if os.path.isdir(filename):
            match = EXTRACT_HEIGHT_SONS_RE.search(filename)
            if match is None:
                raise ValueError(
                    'Error: Unexpected path format: {}'.format(filename))
            block = int(match.group(1))
            height = int(match.group(2))
            num_sons = int(match.group(3))
            roots[block] = calculate_root(filename, height, num_sons)

    return roots


if __name__ == '__main__':

    roots = generate_roots('blocks')

    # roots = generate_roots('.')

    iv = 'a861f335d4d457a7c1d00640da380dc4'
    prev_hash = iv
    for i in range(len(roots)):
        current_data = prev_hash + roots[i].get_hash()
        prev_hash = hashlib.md5(current_data.encode('ascii'
                                                    )).hexdigest()

    print(prev_hash)
