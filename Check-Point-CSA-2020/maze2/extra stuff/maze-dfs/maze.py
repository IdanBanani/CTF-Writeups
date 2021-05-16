import socket
import time
import operator
# from collections import namedtuple
from dataclasses import dataclass
# import numpy as np

from enum import Enum

BOARD_SIZE = 250

UNKNOWN = '.'
BEEN_HERE = 'X'
WALL = '='
DEAD_END = 'D'

class FB(Enum):
    KEEP_GOING = 1
    WALL = 2
    DONT_GO_HERE = 3


class Direction(Enum):
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4
    # NOT_KNOWN = 5


@dataclass
class Cell:
    state: str
    origin: Direction


opposites = {Direction.LEFT: Direction.RIGHT, Direction.RIGHT: Direction.LEFT,
             Direction.UP: Direction.DOWN, Direction.DOWN: Direction.UP
             }


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
#
# offsets = {Direction.UP: (0, 1), Direction.DOWN: (0, -1),
#            Direction.LEFT: (-1, 0), Direction.RIGHT: (1, 0)}

offsets = {Direction.UP: (0, -1), Direction.DOWN: (0, 1),
           Direction.LEFT: (-1, 0), Direction.RIGHT: (1, 0)}

exits = {Borders.UPPER: (Direction.UP,),
         Borders.BUTTOM: (Direction.DOWN,),
         Borders.LEFT: (Direction.LEFT,),
         Borders.RIGHT: (Direction.RIGHT,),
         Borders.UPPER_LEFT: (Direction.LEFT, Direction.UP),
         Borders.BUTTOM_LEFT: (Direction.LEFT, Direction.DOWN),
         Borders.UPPER_RIGHT: (Direction.RIGHT, Direction.UP),
         Borders.BUTTOM_RIGHT: (Direction.RIGHT, Direction.DOWN)}


maze = []
for _ in range(BOARD_SIZE):
    maze.append([Cell(UNKNOWN, None) for _ in range(BOARD_SIZE)])

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


def state_machine():
    input_pos = yield  # get the starting position
    x, y = input_pos
    # global maze

    while True:
        failures = 0
        for action in Direction:

            if BOARD_SIZE - 1 in input_pos or 0 in input_pos:
                invalid_actions = exits[get_border(input_pos)]
            else:
                invalid_actions = tuple()

            x, y = input_pos

            if action == (maze[BOARD_SIZE - 1 - y][x]).origin or action in invalid_actions:
                continue

            dx, dy = offsets[action]
            # dy = -dy
            next_pos = tuple(map(operator.add, ((BOARD_SIZE - 1 - y, x)), ((dy, dx))))
            if (maze[BOARD_SIZE - 1 - next_pos[0]][next_pos[1]]).state == UNKNOWN:
                feedback, input_pos = yield action
                if feedback == FB.KEEP_GOING:
                    x, y = input_pos
                    maze[BOARD_SIZE - 1 - y][x].state = BEEN_HERE
                    maze[BOARD_SIZE - 1 - y][x].origin = opposites[action] # how to go back
                    break
                else:
                    failures = failures + 1
                    if failures == 3:
                        maze[BOARD_SIZE - 1 - y][x].state = DEAD_END
                        yield maze[BOARD_SIZE - 1 - y][x].origin
                        break
                    else:
                        continue

            else:
                #TODO: code duplication!!!
                failures = failures + 1
                if failures == 3:
                    maze[BOARD_SIZE - 1 - y][x].state = DEAD_END
                    yield opposites[maze[BOARD_SIZE - 1 - y][x].origin]
                    break
                else:
                    continue


if __name__ == "__main__":
    game_over = False

    with open('my_maze.txt', 'w') as m, open('maze_output.txt', 'w') as f:
            s = socket.socket()
            try:
                count = 0
                s.connect(('maze.csa-challenge.com', 80))
                start_time = time.time()
                for i in range(10):
                    s.recv(1024)  # skip welcome messages
                pos = eval((s.recv(1024)[68:]).decode("utf-8"))  # tuple, starting point
                msg = s.recv(1024)  # skip 'What is your command?'

                solver = state_machine()
                next(solver)
                curr_move = solver.send(pos)  # works
                f.write(f'Starting point is: {pos}')

                s.send(str.encode(commands[curr_move] + "\n"))

                while True:
                    msg = (s.recv(1024)).decode("utf-8")

                    skip = (s.recv(1024)).decode("utf-8")  # skip  "> What is your command?"
                    if skip != '> What is your command?\n':
                        f.write(skip)
                        print(skip)

                    future_pos = tuple(map(operator.add, pos, offsets[curr_move]))
                    if msg[0] == '1' and len(msg) < 3:

                        pos = future_pos
                        if maze[BOARD_SIZE - pos[1]][pos[0] + 1].state == UNKNOWN:
                            count = count + 1
                            if count % 50 == 0:
                                print(count)

                        curr_move = solver.send(tuple((FB.KEEP_GOING, pos)))
                        s.send(str.encode(commands[curr_move] + "\n"))

                    elif msg[0] == '0' and len(msg) < 3:
                        (maze[BOARD_SIZE - future_pos[1]][future_pos[0] + 1]).state = WALL
                        row = BOARD_SIZE - pos[1]
                        col = pos[0] + 1
                        curr_move = solver.send(tuple((FB.WALL, pos)))
                        s.send(str.encode(commands[curr_move] + "\n"))
                    else:
                        print(skip)
                        print(msg)
                        print(pos)
                        msg = (s.recv(1024)).decode("utf-8")
                        while msg != '':
                            print(msg)
                            msg = (s.recv(1024)).decode("utf-8")
                        game_over = True

                        for line in maze:
                            states = [x.state for x in line]
                            m.write(''.join(states) + '\n')

                        break

                f.write("--- %s seconds ---" % (time.time() - start_time))

            except ValueError:
                pass
            finally:
                s.close()
                game_over = True
