#Strange game, didn't use
from pwn import *
# cube = [
#     [8,1,6],
#     [3,5,7],
#     [4,9,2]
#     ]
#
sum = 15
combinations = set()
for i in range (1,10):
    for j in range(1, 10):
        if j == i: continue
        for k in range(1, 10):
            if k==j or k==i : continue

            if i+j+k == sum:
                combinations.add((i,j,k))
print(len(combinations))


    # print(i,count)

io = remote( 'strange-game.csa-challenge.com',4444)
io.recvuntil('Press any key...')
io.sendline()
used_numbers = set()
for i in range(5):
    header = io.recvuntil('Available moves: ').decode()
    print(header)
    moves = io.recvline().rstrip().decode()
    io.recvuntil('I choose to play ')
    rival_choice = int(io.recv(1))
    used_numbers.add(rival_choice)
    max_i, max = 0,0

    for i in range(1,10):
        if str(i) not in moves or i in used_numbers:
            continue
        count = 0
        for t in combinations:
            if i in t:
                count+=1
            if count > max:
                max = count
                max_i = i


    print(io.recv().decode())
    used_numbers.add((max_i))
    io.sendline(str(max_i))
