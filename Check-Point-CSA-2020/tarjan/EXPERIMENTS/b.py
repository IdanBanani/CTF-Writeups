
from collections import Counter

import string
with open('words.txt') as f:

    lines = f.read()
    c = Counter(lines)
    lines = lines.split('\n')

    clean = [''.join(sorted(line)) for line in lines]
    check = [line for line in sorted(clean)]
seta = set()
# for word in check:

# seta.add(len(word))
print(seta)
print(c)
# print(check)
print(len(check))
print(len(set(check)))

# for c in string.ascii_lowercase:
#     for word in check:
#         if c in word:
#             print(c, end='')
#             break
