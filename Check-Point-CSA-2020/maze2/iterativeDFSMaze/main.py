from __future__ import annotations
import time
from collections import deque

import z3
import re
from pwn import *
from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple
from ctypes import c_ubyte

BOARD_SIZE = 250  # Matrix
finished = False
count = 0
equations_cnt = 0
stack = deque()

# TODO: change int char (byte)
class Location(NamedTuple):
    row: c_ubyte
    col: c_ubyte


class State(Enum):
    NOT_MARKED = '.'
    MARKED = 'X'


class Direction(Enum):
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4


class Special(Enum):
    INFORMATION = 1
    DISTANCE = 2
    HELP = 3
    LOCATION = 4
    SOLUTION = 5


@dataclass
class Cell:
    state: State
    restore_action: Direction
    location: Location
    parent: Cell
    options: int
    failures: int


opposites = {Direction.LEFT: Direction.RIGHT, Direction.RIGHT: Direction.LEFT,
             Direction.UP: Direction.DOWN, Direction.DOWN: Direction.UP
             }

commands = {Direction.UP: 'u', Direction.DOWN: 'd',
            Direction.LEFT: 'l', Direction.RIGHT: 'r',
            Special.INFORMATION: 'i', Special.LOCATION: 'c',
            Special.DISTANCE: 'g', Special.HELP: 'h',
            Special.SOLUTION: 's'}

offsets = {Direction.UP: Location(-1, 0), Direction.DOWN: Location(1, 0),
           Direction.LEFT: Location(0, -1), Direction.RIGHT: Location(0, 1)}

maze = []
for i in range(BOARD_SIZE):
    maze.append([Cell(State.NOT_MARKED, None, Location(i, j), None, 0, 0) for j in range(BOARD_SIZE)])


def get_key(val):
    for key, value in commands.items():
        if val == value:
            return key

    return "key doesn't exist"


def get_next_cell(curr_loc, action):
    next_row = curr_loc.row + offsets[action][0]
    next_col = curr_loc.col + offsets[action][1]
    next_location = Location(next_row, next_col)
    candidate_cell = maze[next_location.row][next_location.col]
    return candidate_cell


def addEquation(dist, loc):
    global equations_cnt

    print(f'#equations: {equations_cnt}')
    # if count > 4000 and dist < 40:
    x, y = loc
    equations_cnt += 1

    z3solver.add(u ** 2 - 2 * u * x + x ** 2 + v ** 2 - 2 * v * y + y ** 2 == dist)
    if equations_cnt > 20:
        if z3solver.check() == z3.sat:
            model = z3solver.model()
            res = f'({model[u]},{model[v]})'
            conn.sendline(commands[Special.SOLUTION])
            help_me_skip()
            conn.sendline(res)
            flag = conn.recvlineS()
            print(flag)
            help_me_skip()
            raise StopIteration


def help_me_skip():
    skip = conn.recvlineS().rstrip()
    if 'What is your' not in skip:
        print(skip)


def game(came_from):
    global count
    conn.sendline(commands[Special.LOCATION])
    # conn.recvuntil(b' ', drop=True)
    loc = eval(conn.recvlineS().rstrip())
    row, col = BOARD_SIZE - 1 - loc[1], loc[0]
    maze_loc = Location(row, col)
    maze[row][col].state = State.MARKED
    help_me_skip()

    conn.sendline(commands[Special.DISTANCE])
    dist = conn.recvlineS().rstrip()
    help_me_skip()

    if dist.find('Your distance from the treasure is') != -1:
        dist = int(re.search(r'\d+', dist).group())
        print('dist: ', dist)
        addEquation(dist, loc)

    count += 1
    print(count, end='|')
    if count % 30 == 0:
        print('')
    conn.sendline(commands[Special.INFORMATION])
    # msg = (sock.recv(INFO_LEN)).decode("utf-8")
    msg = conn.recvlineS().rstrip()
    msg = msg.replace(' ', '')
    msg = msg.split(',')
    moves = [d[0] for d in msg if d[-1] == '1']

    help_me_skip()
    for move in moves:

        next_cell = get_next_cell(maze_loc, get_key(move))
        # print(moves, move, 'loc:',maze_loc,'next cell ', next_cell.location,next_cell.state)
        if next_cell.state == State.NOT_MARKED and move != came_from:
            conn.sendline(move)
            # feedback = conn.recvlineS().rstrip()
            # print(feedback)
            conn.recvline()
            help_me_skip()
            game(commands[opposites[get_key(move)]])

    if came_from != None:
        conn.sendline(came_from)
        msg = conn.recvlineS().rstrip()
        help_me_skip()

    return


if __name__ == "__main__":

    INFO_LEN = len('l=0, r=1, u=0, d=0\n')
    try:
        conn = remote('maze.csa-challenge.com', 80)
        start_time = time.time()
        for i in range(10):
            conn.recvline()

        pos = eval(conn.recvlineS().rstrip()[68:])  # tuple, starting point
        live_location = Location(BOARD_SIZE - 1 - pos[1], pos[0])
        print(f'Starting point is: {pos} which is {live_location} in the matrix')
        first_node = maze[live_location.row][live_location.col]

        u = z3.Int('u')
        v = z3.Int('v')
        z3solver = z3.Solver()
        help_me_skip()

        # sta
        game(None)
        print("--- %s seconds ---" % (time.time() - start_time))

    except ValueError:
        pass
    finally:
        conn.close()
        game_over = True
