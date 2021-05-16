from itertools import product


def randString(istr):
    l = [(c, c.upper()) if not c.isdigit() else (c,) for c in istr.lower()]
    return ["".join(item) for item in product(*l)]


words = randString('jane')

with open('tree.txt') as f:
    dirty = f.read()
    indexes = []
    for word in words:
        res = 0
        try:
            while 1:
                res = dirty.index(word, res)
                indexes.append(tuple((res, res+3)))
                # print(res)
                # print(dirty[res:res+100])
                res = res+3

        except ValueError:
            pass
    # c = Counter(dirty)
    # result = re.sub('[^0-9]', '', dirty)
    # print(result)
    for t in indexes:
        print(t)
