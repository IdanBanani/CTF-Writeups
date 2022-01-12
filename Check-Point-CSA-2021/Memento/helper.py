import itertools
flag = [
    ['n'],
['e',],
['i', 'r'],
['e', 'n', 'w'],
['e', 'n', 'w'],
['_'],
['a', 'j', 's'],
['c', 'l', 'u'],
['c', 'l', 'u'],
['e', 'n', 'w'],
['e', 'n', 'w'],
['e', 'n', 'w'],
['e', 'n', 'w'],
['d', 'm', 'v'],
['_'] ,
['d', 'm', 'v'],
['i', 'r'],
['i', 'r'],
['i', 'r'],
['f', 'o', 'x'],
['i', 'r'],
['a', 'j', 's'],
['b', 'k', 't'],
['d', 'm', 'v']
]

for x in itertools.product(*flag):
    s = ''.join(x)

    print(s)