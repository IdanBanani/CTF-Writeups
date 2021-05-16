from __future__ import annotations
import socket
import time
import z3
import re
from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple

BOARD_SIZE = 250  # Matrix
finished = False
count =0

# TODO: change int char (byte)
class Location(NamedTuple):
    row: int
    col: int


class State(Enum):
    NOT_MARKED = '.'
    MARKED = 'X'


class FB(Enum):
    KEEP_GOING = 1
    FAR_FAR_AWAY = 2
    FINISH_HIM = 3
    WALL = 4


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


def finish_move(sock, solution=None):
    if solution == None:
        sock.send(str.encode(commands[Special.LOCATION] + "\n"))
        solution = (sock.recv(1024)).decode("utf-8")
        print(solution)
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        msg = (sock.recv(1024)).decode("utf-8").rstrip()
        print(msg)

    sock.send(str.encode(commands[Special.SOLUTION] + "\n"))



def addEquation(dist):
    global equations_cnt
    global loc
    print(f'#equations: {equations_cnt}')
    # if count > 4000 and dist < 40:
    x,y = loc
    equations_cnt += 1

    z3solver.add(u ** 2 - 2 * u * x + x ** 2 + v ** 2 - 2 * v * y + y ** 2 == dist)
    if equations_cnt > 1000:
        if z3solver.check() == z3.sat:
            model = z3solver.model()
            res = f'({model[u]},{model[v]})'

def help_me_skip():
    skip = (sock.recv(1024)).decode("utf-8").rstrip()  # skip  "> What is your command?"
    while 'What is your command?' in skip:
        skip = (sock.recv(1024)).decode("utf-8").rstrip()


def game(came_from):
    global count
    help_me_skip()

    sock.send(str.encode(commands[Special.LOCATION] + "\n"))
    loc = eval((sock.recv(10)).decode("utf-8").rstrip())
    x, y = BOARD_SIZE - 1 - loc[1], loc[0]
    maze_loc = Location(x,y)
    maze[x][y].state = State.MARKED
    help_me_skip()

    sock.send(str.encode(commands[Special.DISTANCE] + "\n"))
    dist = (sock.recv(1024)).decode("utf-8").rstrip()
    if dist.find('Your distance from the treasure is') != -1:
        dist = int(re.search(r'\d+', dist).group())
        print('dist: ',dist)
        addEquation(dist)

    help_me_skip()

    count+=1
    print(count,end='|')
    sock.send(str.encode(commands[Special.INFORMATION] + "\n"))
    msg = (sock.recv(INFO_LEN)).decode("utf-8")
    msg = msg.rstrip().replace(' ', '')
    msg = msg.split(',')
    options = [d[0] for d in msg if d[-1] == '1']
    print(options)
    help_me_skip()
    for move in options:
        next_cell = get_next_cell(maze_loc,get_key(move))
        if next_cell.state == State.NOT_MARKED and  move != came_from:
            sock.send(str.encode(move + "\n"))
            feedback = (sock.recv(1024)).decode("utf-8").split('\n')
            msg = feedback[0] # '1'
            flag = feedback[1]
            print(msg,flag)
            game(commands[opposites[get_key(move)]])
            help_me_skip()

    if came_from != None:
        sock.send(str.encode(came_from + "\n"))
        msg = (sock.recv(1024)).decode("utf-8").rstrip() # '1'
        help_me_skip()

    return








if __name__ == "__main__":

    INFO_LEN = len('l=0, r=1, u=0, d=0\n')
    sock = socket.socket()
    sock.settimeout(60)
    # game_over = false
    try:
        sock.connect(('maze.csa-challenge.com', 80))
        start_time = time.time()
        for i in range(10):
            sock.recv(1024)  # skip welcome messages

        pos = eval((sock.recv(1024).decode("utf-8")[68:]))  # tuple, starting point
        live_location = Location(BOARD_SIZE - 1 - pos[1], pos[0])
        print(f'Starting point is: {pos} which is {live_location} in the matrix')
        first_node = maze[live_location.row][live_location.col]
        equations_cnt = 0
        u = z3.Int('u')
        v = z3.Int('v')
        z3solver = z3.Solver()

        game(None)
        print("--- %s seconds ---" % (time.time() - start_time))

    except ValueError:
        pass
    finally:
        sock.close()
        game_over = True
