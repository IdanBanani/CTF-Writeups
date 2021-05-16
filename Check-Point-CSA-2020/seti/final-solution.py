import string

from collections import defaultdict
from pprint import pprint


def exists(a, sub_sequence):
    """checks if b exists in a as a subsequence"""
    pos = 0
    for ch in a:
        if pos < len(sub_sequence) and ch == sub_sequence[pos]:
            pos += 1
    return pos == len(sub_sequence)


def exists2(partial, code_word):
    it = iter(code_word)
    all(x in it for x in partial)


def string2bits(s=''):
    return ''.join([bin(ord(x))[2:].zfill(8) for x in s])


def bits2string(b=None):
    return ''.join([chr(int(x, 2)) for x in b])


def process(partial, counters):
    for t in mapping_set:
        code_word, c = t
        if exists(code_word, partial):
            counters[c] += 1


def max_values(counters):
    # Find item with Max Value in Dictionary
    itemMaxValue = max(counters.items(), key=lambda x: x[1])
    # print('Maximum Value in Dictionary : ', itemMaxValue[1])
    listOfKeys = list()
    # Iterate over all the items in dictionary to find keys with max value
    for key, value in counters.items():
        if value == itemMaxValue[1]:
            listOfKeys.append(key)

    return listOfKeys


# my_str = "Bang, zoom, straight to the moon!"
dictionary = string.printable
mapping_set = {((string2bits(c), c)) for c in dictionary}

# with open('first_signal.txt') as f:
with open('second_signal.txt') as f:
    message = ''
    original = f.read()
    main_lst = eval(original)
    for i, signal in enumerate(main_lst):
        counters = defaultdict(int)
        sl = []

        for defected in signal:
            as_str = ''.join([str(x) for x in defected])
            process(as_str, counters)

        options = max_values(counters)

        new_answer = []
        for option in options:
            new_answer.append(option)
        if len(options) == 1:
            message += options[0] + '\n'
        else:
            message += '[' + '|'.join(options) + ']\n'

    print(message)
