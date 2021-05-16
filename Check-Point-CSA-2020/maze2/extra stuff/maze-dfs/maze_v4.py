from __future__ import annotations
import socket
import time
import operator
# from collections import namedtuple
from dataclasses import dataclass
# import numpy as np

from enum import Enum
from queue import LifoQueue
from typing import NamedTuple


BOARD_SIZE = 250


# TODO: change int char (byte)
class Location(NamedTuple):
    row: int
    col: int


class State(Enum):
    NOT_MARKED = '.'
    MARKED = 'X'


class FB(Enum):
    KEEP_GOING = 1
    WALL = 2


class Direction(Enum):
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4


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


offsets = {Direction.UP: Location(-1, 0), Direction.DOWN: Location(1, 0),
           Direction.LEFT: Location(0, -1), Direction.RIGHT: Location(0, 1)}

exits = {Borders.UPPER: (Direction.UP,),
         Borders.BUTTOM: (Direction.DOWN,),
         Borders.LEFT: (Direction.LEFT,),
         Borders.RIGHT: (Direction.RIGHT,),
         Borders.UPPER_LEFT: (Direction.LEFT, Direction.UP),
         Borders.BUTTOM_LEFT: (Direction.LEFT, Direction.DOWN),
         Borders.UPPER_RIGHT: (Direction.RIGHT, Direction.UP),
         Borders.BUTTOM_RIGHT: (Direction.RIGHT, Direction.DOWN)}

maze = []
for i in range(BOARD_SIZE):
    maze.append([Cell(State.NOT_MARKED, None, Location(i, j), None, 4, 0) for j in range(BOARD_SIZE)])


def get_border(pos):
    x, y = pos
    print(f'checking border at', pos)
    if x == BOARD_SIZE - 1:
        if y == BOARD_SIZE - 1:
            return Borders.BUTTOM_RIGHT
        elif y == 0:
            return Borders.BUTTOM_LEFT
        else:
            return Borders.BUTTOM

    elif x == 0:
        if y == BOARD_SIZE - 1:
            return Borders.UPPER_RIGHT
        elif y == 0:
            return Borders.UPPER_LEFT
        else:
            return Borders.UPPER

    else:
        if y == 0:
            return Borders.LEFT
        else:
            return Borders.RIGHT


def state_machine():

    global maze
    current_node = yield
    current_node.state = State.MARKED

    curr_loc = current_node.location
    stack = LifoQueue()

    for action in Direction:
        next_row = curr_loc.row + offsets[action][0]
        next_col = curr_loc.col + offsets[action][1]
        next_location = Location(next_row, next_col)

        candidate_cell = maze[next_location.row][next_location.col]
        candidate_cell.state = State.MARKED

        candidate_cell.parent = current_node
        candidate_cell.restore_action = opposites[action]  # TODO: remove, no effect
        stack.put((action, candidate_cell))

    # failures = 0

    while not stack.empty():

        if (current_node.failures == current_node.options):
            current_node.parent.failures = current_node.parent.failures + 1
            dummy = yield current_node.restore_action, current_node.parent
            current_node = current_node.parent
            continue

        action, candidate_cell = stack.get()
        feedback = yield action, candidate_cell

        if feedback == FB.KEEP_GOING:

            current_node = candidate_cell
            current_node.options = 4
            current_node.failures = 0

            curr_loc = current_node.location
            if BOARD_SIZE - 1 in curr_loc or 0 in curr_loc:
                invalid_actions = exits[get_border(curr_loc)]
            else:
                invalid_actions = tuple()

            for action in Direction:
                if action == current_node.restore_action or action in invalid_actions:
                    current_node.options = current_node.options - 1
                    continue

                next_row = curr_loc.row + offsets[action][0]
                next_col = curr_loc.col + offsets[action][1]
                next_location = Location(next_row, next_col)
                print(next_location)
                candidate_cell = maze[next_location.row][next_location.col]

                if candidate_cell.state == State.NOT_MARKED:
                    candidate_cell.state = State.MARKED
                    candidate_cell.parent = current_node
                    candidate_cell.restore_action = opposites[action]
                    stack._put((action, candidate_cell))
                else:
                    current_node.options = current_node.options - 1

            if 0 == current_node.options:
                # print('going back2')
                # stack._put((current_node.restore_action, current_node.parent))
                current_node.parent.failures = current_node.parent.failures + 1

                dummy = yield current_node.restore_action, current_node.parent


        else:
            current_node.failures = current_node.failures + 1

            # print(current_node.failures)
            # if current_node.failures == current_node.options:
            #     current_node.parent.failures = current_node.parent.failures + 1
            #     dummy = yield current_node.restore_action, current_node.parent


if __name__ == "__main__":

    with open('my_maze.txt', 'w') as m, open('maze_output.txt', 'w') as f:
        s = socket.socket()
        try:

            s.connect(('maze.csa-challenge.com', 80))
            start_time = time.time()
            for i in range(10):
                s.recv(1024)  # skip welcome messages
            pos = eval((s.recv(1024)[68:]).decode("utf-8"))  # tuple, starting point
            live_location = Location(BOARD_SIZE - 1 - pos[1], pos[0])  # First location
            # live_location = Location( pos[1], pos[0])  # First location
            print(f'Starting point is: {pos} which is {live_location} in the matrix')
            curr_node = maze[live_location.row][live_location.col]

            msg = s.recv(1024)  # skip 'What is your command?'

            solver = state_machine()  # got the closure inner
            next(solver)
            next_move, future_node = solver.send(curr_node)  # get the first 'try' move
            s.send(str.encode(commands[next_move] + "\n"))

            while True:

                msg = (s.recv(1024)).decode("utf-8")
                skip = (s.recv(1024)).decode("utf-8")  # skip  "> What is your command?"
                if skip != '> What is your command?\n':
                    f.write(skip)
                    print('unique message:',skip)

                if msg[0] == '1' and len(msg) < 3:
                    curr_node = future_node
                    # print(curr_node.location)
                    next_move, future_node = solver.send(FB.KEEP_GOING)
                    s.send(str.encode(commands[next_move] + "\n"))

                elif msg[0] == '0' and len(msg) < 3:
                    next_move, future_node = solver.send(FB.WALL)
                    s.send(str.encode(commands[next_move] + "\n"))
                else:
                    print('special:',skip)
                    print('special:',msg)
                    # print(pos)
                    msg = (s.recv(1024)).decode("utf-8")
                    while msg != '':
                        print(msg)
                        msg = (s.recv(1024)).decode("utf-8")

                    # for line in maze:
                    #     states = [x.state for x in line]
                    #     m.write(''.join(states) + '\n')

                    break

            f.write("--- %s seconds ---" % (time.time() - start_time))

        except ValueError:
            pass
        finally:
            s.close()
            game_over = True
