import math


def LCA(idx1, idx2):

    print(idx1, idx2)
    log1 = int(math.log2(idx1))
    log2 = int(math.log2(idx2))
    bigger, smaller = ((idx1, idx2)) if log1 == max(
        log1, log2) else ((idx2, idx1))

    if log1 != log2:
        while(int(math.log2(bigger)) != int(math.log2(smaller))):
            bigger //= 2

    while bigger != smaller:
        if bigger == 1:
            break

        bigger //= 2
        smaller //= 2

    print(bigger)
    return bigger


with open('tree.txt', 'r') as t, open('pairs.txt', 'r') as p:
    tree = t.read().rstrip()
    pairs = eval(p.read().rstrip())

# print(my_tree.pop(), ": popped")
answer = []

for x, y in pairs:
    answer.append(tree[LCA(x+1, y+1) - 1])

print(''.join(answer))
