import string

from collection import defaultdict
from pprint import pprint


def exists(a, b):
    """checks if b exists in a as a subsequence"""
    pos = 0
    for ch in a:
        if pos < len(b) and ch == b[pos]:
            pos += 1
    return pos == len(b)


def exists2(partial, code_word):
    it = iter(code_word)
    all(x in it for x in partial)


def string2bits(s=''):
    return [bin(ord(x))[2:].zfill(8) for x in s]


def bits2string(b=None):
    return ''.join([chr(int(x, 2)) for x in b])


my_str = "Bang, zoom, straight to the moon!"
dictionary = string.printable
mapping_set = {((string2bits(c), c)) for c in dictionary}

counters = defaultdict()


def process(partial):
    for t in mapping_set:


with open('first_signal.txt') as f:

    original = f.read()
    chars_set = set()
    lengths = []
    rows = []
    main_lst = eval(original)
    print(f'outer len: {len(main_lst)}')
    for i, sub_list in enumerate(main_lst):
        sl = []

        print(i, len(sub_list), my_str[i])

