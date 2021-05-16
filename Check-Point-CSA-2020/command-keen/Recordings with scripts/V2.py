import os

# filelist = os.listdir()
# filelist = sorted(filelist, key=lambda x: int(os.path.splitext(x)[0]))
# filelist.sort(key=lambda f: int(filter(str.isdigit, f)))

count = 0

moves = []
x = {-127: 'L', 127: 'R', 0: ''}
y = {-127: 'D', 127: 'U', 0: ''}

for file in sorted(os.listdir(os.getcwd()), key=lambda x: int(x.replace(".BIN", ""))):
    with open(file, 'rb') as f, open('./out/'+'out'+str(count)+'.txt', 'w') as o:
        line = bytearray(f.read(8))
        while (line):
            moves.append(line)
            line = f.read(8)

    # print(moves)
    for move in moves:
        count = int.from_bytes(move[:2], byteorder='little', signed=True)
        x_direction = x[int.from_bytes(
            move[4:6], byteorder='little', signed=True)]
        y_direction = y[int.from_bytes(
            move[6:], byteorder='little', signed=True)]
        if x_direction != '' and y_direction != '':
            o.write(count, y_direction, d_direction)
    count += 1
