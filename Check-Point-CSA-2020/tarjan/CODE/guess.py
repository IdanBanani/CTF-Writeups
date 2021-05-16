next = '0b111000'
left = False
print(12, next)
for i in range(13, 47):

    if left:
        next = int(next, 2) << 1
        next = next - 1
    else:
        next = int(next, 2) >> 1
        next = next + 1

    next = bin(next)
    print(i, next)
    left = not left
