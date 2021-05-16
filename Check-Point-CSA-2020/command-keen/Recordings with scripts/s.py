moves = []

x = {-127: 'L', 127: 'R', 0: ''}
y = {-127: 'D', 127: 'U', 0: ''}
with open('2.BIN', 'rb') as f:
    line = bytearray(f.read(8))
    while (line):
        moves.append(line)
        line = f.read(8)

count = 0
# print(moves)
for move in moves:
    steps = int.from_bytes(move[:2], byteorder='little', signed=True)
    x_direction = x[int.from_bytes(move[4:6], byteorder='little', signed=True)]
    y_direction = y[int.from_bytes(move[6:], byteorder='little', signed=True)]
    if x_direction != '' or y_direction != '':
        count += 1
        print(f'{steps} {x_direction}{y_direction}', end='  ')

        if count % 5 == 0:
            print('')
