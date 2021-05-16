from os import listdir
from os.path import isfile, join
import hashlib


def calculate_row_above(layer_underneath_nodes, sons):


    current_tree_row = []

    #   Y      Y
    # X X X  X X X

    # calculate upper level node
    for i in range(0, len(layer_underneath_nodes), sons):
        children_hash_concat = ""

        for j in range(i, i + sons):
            children_hash_concat += layer_underneath_nodes[j]

        mm = hashlib.md5(children_hash_concat.encode('utf-8'))
        current_tree_row += [mm.hexdigest()] #add to queue

    return current_tree_row


def main():

    IV = 'a861f335d4d457a7c1d00640da380dc4'
    prev = IV
    mypath = './blocks'
    files_lst = listdir(mypath)

    leaves_queue = []
    #for each tree
    for folder in files_lst:    # fold: block_0-height_1-sons_2

        leaf_data_full_path = mypath + '/' + folder + '/'

        folder = folder.split("-")

        # tree_height = int((folder[1].split("_"))[1])
        tree_num_sons = int((folder[2].split("_"))[1])


        leaves_tx_data = listdir(leaf_data_full_path)

        leaves_tx_data.sort(key=len)

        for tx in leaves_tx_data:
            with open(leaf_data_full_path + tx, "r") as f:
                leaves_queue.append(f.read())


        for i in range(len(leaves_queue)):
            leaves_queue[i] = hashlib.md5(leaves_queue[i].encode('ascii')).hexdigest()


        while len(leaves_queue) != 1:
            leaves_queue = calculate_row_above(leaves_queue, tree_num_sons)


        # After the last step of hashit - there is only md5 of root in the queue
        ins = leaves_queue.pop()
        prev = hashlib.md5((prev+ins).encode('utf-8')).hexdigest()

    print(prev)


if __name__ == '__main__':
    main()
