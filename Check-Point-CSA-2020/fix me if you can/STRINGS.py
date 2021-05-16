import string


def strings(filename, min=4):
    with open(filename, errors="ignore") as f:  # Python 3.x
        # with open(filename, "rb") as f:           # Python 2.x
        result = ""
        for c in f.read():
            if c in string.printable:
                result += c
                continue
            if len(result) >= min:
                yield result
            result = ""
        if len(result) >= min:  # catch result at EOF
            yield result


# with open('Fix_me.doc', 'rb') as f:
#     data = f.read()
#     data = data[::-1]
#     with open('new.doc', 'wb') as g:
#         g.write(data)


sl = list(strings("Fix_me.doc"))
print(sl)
