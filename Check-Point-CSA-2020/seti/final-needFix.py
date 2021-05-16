import string

from collections import defaultdict
from pprint import pprint


def exists(a, sub_sequence, treshold):
    pos = 0
    count = 0
    while pos < 8 and count < len(sub_sequence):
        if a[pos] == sub_sequence[count]:
            count += 1
        pos += 1
    return count == treshold


def exists2(partial, code_word):
    it = iter(code_word)
    all(x in it for x in partial)


def string2bits(s=''):
    return ''.join([bin(ord(x))[2:].zfill(8) for x in s])


def bits2string(b=None):
    return ''.join([chr(int(x, 2)) for x in b])


def process(partial, counters, treshold):
    results = 0
    for t in mapping_set:
        code_word, c = t
        if exists(code_word, partial, treshold):
            counters[c] += 1
            results += 1
    if results == 0:
        process(partial, counters, treshold-1)


def max_values(counters):
    # Find item with Max Value in Dictionary
    listOfKeys = list()

    itemMaxValue = max(counters.items(), key=lambda x: x[1])
    # print('Maximum Value in Dictionary : ', itemMaxValue[1])

    # Iterate over all the items in dictionary to find keys with max value
    for key, value in counters.items():
        if value == itemMaxValue[1]:
            listOfKeys.append(key)

    return listOfKeys


dictionary = string.printable + ' '
mapping_set = {((string2bits(c), c)) for c in dictionary}
answers = ['']


with open('second_signal.txt') as f:
    message = ''
    original = f.read()
    main_lst = eval(original)
    print(len(main_lst))
    for i, signal in enumerate(main_lst):
        counters = defaultdict(int)

        for defected in signal:
            as_str = ''.join([str(x) for x in defected])
            process(as_str, counters, 6)

        options = max_values(counters)

        new_answer = []
        for option in options:
            for answer in answers:
                new_answer.append(answer+option)

        if len(options) == 1:
            message += options[0] + '\n'
        else:
            message += '[' + '|'.join(options) + ']\n'

    splitted = message.split('\n')
    for i, l in enumerate(splitted):
        if 15 <= i <= 30:
            print(i, l)
