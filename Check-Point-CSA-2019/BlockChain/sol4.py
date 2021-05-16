import hashlib
import os

#for one tree
def calculate_block(b_dir):
    encoding_method = 'ascii'

    base, cur_dir = b_dir.split('\\') # OS dependent? - not good
    splitted_dir = cur_dir.split('-')
    height = int(splitted_dir[1][-1:])
    sons = int(splitted_dir[2][-1:])

    current_row_hashes = []

    files_id = []

    for filename in os.listdir(b_dir):
        filename = filename.split('_')
        files_id.append(int(filename[1]))

    files_id.sort()

    filenames = []
    for filename in files_id:
        filenames.append('tx_{0}'.format(filename))


    # save leafs
    # for filename in os.listdir(b_dir):
    for filename in filenames:
        # print filename
        file_content = open(b_dir + '\\' + filename, 'r').read()

        node_hash = hashlib.md5(file_content.encode(encoding_method)).hexdigest()
        current_row_hashes.append(node_hash)

    # now calculate the block root
    above_row_hashes = []



    while height > 0:

        start_index = 0
        while start_index < len(current_row_hashes):
            node_hash = ''

            for i in range(sons):
                node_hash += current_row_hashes[start_index + i]

            node_hash = hashlib.md5(node_hash.encode(encoding_method)).hexdigest()
            above_row_hashes.append(node_hash)
            start_index += sons


        current_row_hashes = above_row_hashes   # list_a
        above_row_hashes = []                   # list_
        height -= 1

    return current_row_hashes[0] #return root

if __name__ == '__main__':
    encoding_method = 'ascii'
    prev_hash = 'a861f335d4d457a7c1d00640da380dc4'

    for block_dir in os.listdir('blocks'):
        calculated_hash = calculate_block('blocks\\' + block_dir)
        prev_hash = hashlib.md5((prev_hash + calculated_hash).encode(encoding_method)).hexdigest()

    print(prev_hash)