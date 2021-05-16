import socket
import time
import operator
# from collections import namedtuple
from recordtype import recordtype

import numpy as np
from enum import Enum

BOARD_SIZE = 250

UNKNOWN = '.'
BEEN_HERE = 'X'
WALL = '='
SPLIT_POINT = 'S'
DEAD_END = 'D'
BEGINNING = 'B'


class FB(Enum):
    KEEP_GOING = 1
    WALL = 2
    DONT_GO_HERE = 3


class Direction(Enum):
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4
    NOT_KNOWN = 5


opposites = {Direction.LEFT: Direction.RIGHT, Direction.RIGHT: Direction.LEFT,
             Direction.UP: Direction.DOWN, Direction.DOWN: Direction.UP}


class Borders(Enum):
    UPPER = 1
    BUTTOM = 2
    LEFT = 3
    RIGHT = 4
    UPPER_LEFT = 5
    UPPER_RIGHT = 6
    BUTTOM_LEFT = 7
    BUTTOM_RIGHT = 8


commands = {Direction.UP: 'u', Direction.DOWN: 'd',
            Direction.LEFT: 'l', Direction.RIGHT: 'r'}

offsets = {Direction.UP: (0, 1), Direction.DOWN: (0, -1),
           Direction.LEFT: (-1, 0), Direction.RIGHT: (1, 0)}

exits = {Borders.UPPER: (Direction.UP,),
         Borders.BUTTOM: (Direction.DOWN,),
         Borders.LEFT: (Direction.LEFT,),
         Borders.RIGHT: (Direction.RIGHT,),
         Borders.UPPER_LEFT: (Direction.LEFT, Direction.UP),
         Borders.BUTTOM_LEFT: (Direction.LEFT, Direction.DOWN),
         Borders.UPPER_RIGHT: (Direction.RIGHT, Direction.UP),
         Borders.BUTTOM_RIGHT: (Direction.RIGHT, Direction.DOWN)}

# maze = np.full((BOARD_SIZE - 1, BOARD_SIZE - 1), ((UNKNOWN, Direction.NOT_KNOWN)))
cell = recordtype('Cell',['state','origin'])
empty_cell = cell(UNKNOWN,Direction.NOT_KNOWN)
maze = [ [empty_cell for i in range (BOARD_SIZE) ] for j in range (BOARD_SIZE)]
print (len(maze))
print (len(maze[0]))
def get_border(pos):
    x, y = pos
    print(f'checking border at', pos)
    if x == BOARD_SIZE - 1:
        if y == BOARD_SIZE - 1:
            return Borders.UPPER_RIGHT
        elif y == 0:
            return Borders.BUTTOM_RIGHT
        else:
            return Borders.RIGHT

    elif x == 0:
        if y == BOARD_SIZE - 1:
            return Borders.UPPER_LEFT
        elif y == 0:
            return Borders.BUTTOM_LEFT
        else:
            return Borders.LEFT

    else:
        if y == 0:
            return Borders.BUTTOM
        else:
            return Borders.UPPER


# def count_options(start_pos):
#     cnt = 0
#     for act in Direction:
#         feedback, input_pos, input_cube = yield act
#         if feedback == FB.KEEP_GOING:
#             cnt = cnt + 1
#             yield opposites[act] #go back to starthing point
#
#     return cnt


def state_machine():
    input_pos = yield  # get the starting position
    failures = 0
    global maze
    # make the first succesful move
    trial_action = None
    feedback = None
    # options = count_options(input_pos)
    # maze[input_pos] = DEAD_END if options == 1
    while True:
        failures = 0
        for action in Direction:

            if BOARD_SIZE - 1 in input_pos or 0 in input_pos:
                invalid_actions = exits[get_border(input_pos)]
            else:
                invalid_actions = tuple()

            x, y = input_pos

            if action == (maze[BOARD_SIZE-1 - y][x])[1] or action in invalid_actions:
                continue

            dx, dy = offsets[action]
            dy = -dy
            next_pos = tuple(map(operator.add, ((BOARD_SIZE-1 - y, x)), ((dy, dx))))
            if (maze[BOARD_SIZE-1 - next_pos[0]] [next_pos[1]])[0] == UNKNOWN:
                feedback, input_pos = yield action
            else:
                failures = failures + 1
                if failures == 3:
                    maze[input_pos][0] = DEAD_END
                    yield opposites[maze[input_pos][1]]
                    break
                else:
                    continue

            if feedback == FB.KEEP_GOING:
                failures = 0
                maze[input_pos][0] = BEEN_HERE
                maze[input_pos][1] = action
                break


if __name__ == "__main__":
    game_over = False

    with open('my_maze.txt', 'w') as m, open('maze_output.txt', 'w') as f:
        while not game_over:
            # maze = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=np.int8)
            # maze = np.full((BOARD_SIZE + 2, BOARD_SIZE + 2), UNKNOWN)
            s = socket.socket()

            try:
                count = 0
                s.connect(('maze.csa-challenge.com', 80))
                start_time = time.time()
                for i in range(10):
                    s.recv(1024)  # skip welcome messages
                pos = eval((s.recv(1024)[68:]).decode(
                    "utf-8"))  # tuple, starting point
                msg = s.recv(1024)  # skip 'What is your command?'

                solver = state_machine()
                next(solver)
                curr_move = solver.send(pos)  # works
                f.write(f'Starting point is: {pos}')

                # maze[BOARD_SIZE - pos[1], pos[0] + 1] = START  # starting point
                # maze[BOARD_SIZE - pos[1], pos[0] + 1] = START  # starting point

                s.send(str.encode(commands[curr_move] + "\n"))

                while True:

                    msg = (s.recv(1024)).decode("utf-8")
                    # skip the "> What is your command?"
                    skip = (s.recv(1024)).decode("utf-8")
                    if skip != '> What is your command?\n':
                        f.write(skip)
                        print(skip)

                    future_pos = tuple(map(operator.add, pos, offsets[curr_move]))
                    if msg[0] == '1' and len(msg) < 3:

                        pos = future_pos
                        if maze[BOARD_SIZE - pos[1], pos[0] + 1] == UNKNOWN:
                            maze[BOARD_SIZE - pos[1], pos[0] + 1] = BEEN_HERE
                            count = count + 1
                            if count % 50 == 0:
                                print(count)

                            # if time.time() - start_time > 30:
                            #     game_over = True
                            #     raise ValueError('Hi')

                        # row = BOARD_SIZE - pos[1]
                        # col = pos[0] + 1
                        # cube = maze[row - 1:row + 2, col - 1:col + 2]

                        curr_move = solver.send(tuple((FB.KEEP_GOING, pos)))
                        s.send(str.encode(commands[curr_move] + "\n"))

                    elif msg[0] == '0' and len(msg) < 3:
                        (maze[BOARD_SIZE - future_pos[1]] [future_pos[0] + 1]).state = WALL
                        row = BOARD_SIZE - pos[1]
                        col = pos[0] + 1
                        # cube = maze[row - 1:row + 2, col - 1:col + 2]
                        curr_move = solver.send(tuple((FB.WALL, pos, cube)))
                        s.send(str.encode(commands[curr_move] + "\n"))
                    else:
                        print(skip)
                        print(msg)

                        print(pos)
                        # print(cube)

                        msg = (s.recv(1024)).decode("utf-8")
                        while msg != '':
                            print(msg)
                            msg = (s.recv(1024)).decode("utf-8")
                        game_over = True
                        break

                f.write("--- %s seconds ---" % (time.time() - start_time))

            except ValueError:
                pass
            finally:

                # maze_as_list = maze.tolist()
                # for line in maze:
                #     m.write(''.join(line) + '\n')

                s.close()
                game_over = True
