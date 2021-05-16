import hashlib
import os
import itertools

IV = "a861f335d4d457a7c1d00640da380dc4"
last_block_hash = IV


def hasher(h):
    hx = hashlib.md5()
    hx.update(h.encode('ascii'))  # my small fix (encode)
    return hx.hexdigest()


blocks_dir_path = os.path.join(os.getcwd(),'blocks')
#r=root, d=directories, f=files
for r, d, f in os.walk(blocks_dir_path):

    # for every directory .... different leaves and height
    for directory in d:

      # ditch out the cache folder, should use regular expressions instead to filter
        if 'block' not in directory:
            continue

        block_num, height, sons = [int(x.split("_")[1])  for x in directory.split("-")]

        prev_layer_hashes = [""] * (sons ** height)

        # getting tree leaves
        for tx_num in range(sons ** height):
            with open(os.path.join(
                    blocks_dir_path, directory, "tx_"+str(tx_num)), "r") as tx:
                tx_content = tx.read()
                prev_layer_hashes[tx_num] = hasher(tx_content)

        # perpetually hashing until we get to root
        current_depth = height

        while current_depth != 0:

            tree_layer_above = [""] * (sons ** (current_depth - 1) )  # ascending 1 height

            # hash the current nodes in this row
            for i in range(len(tree_layer_above)):

                tree_layer_above[i] = hasher("".join(itertools.islice(prev_layer_hashes, i * sons, (i + 1) * sons)))

            prev_layer_hashes = tree_layer_above
            current_depth = current_depth - 1

        prev_layer_hashes = prev_layer_hashes.pop()
        last_block_hash = hasher(last_block_hash + prev_layer_hashes)

print(last_block_hash)
