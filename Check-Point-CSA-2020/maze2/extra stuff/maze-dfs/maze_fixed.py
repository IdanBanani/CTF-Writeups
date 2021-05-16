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

#

count = 0
BOARD_SIZE = 250


# stack = None
# flag = True
# solver = None
feedback = None

# TODO: change int char (byte)
class Location(NamedTuple):
    row: int
    col: int


class State(Enum):
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
    state: State
    restore_action: Direction
    location: Location
    parent: Cell


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
    maze.append([Cell(State.UNKNOWN, None, Location(i, j), None) for j in range(BOARD_SIZE)])


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


# def init_dfs():
#     global flag
#     first_cell = yield
# # how to go back
#             # stack._put(second_node)
#             # print(5)
#             flag = False
#             print('flag is now false')
#
#             yield
#             break


def state_machine():
    global count
    global maze
    global feedback
    current_node = yield
    current_node.state = State.DEAD_END
    curr_loc = current_node.location
    stack = LifoQueue()

    for action in Direction:
        next_row = curr_loc.row + offsets[action][0]
        next_col = curr_loc.col + offsets[action][1]
        next_location = Location(next_row, next_col)
        candidate_cell = maze[next_location.row][next_location.col]
        stack.put(candidate_cell)
        # feedback = yield action, candidate_cell
        # if feedback == FB.KEEP_GOING:
        #     current_node.parent = current_node
        #     current_node = candidate_cell
        #     current_node.restore_action = opposites[action]
        #     stack.put(current_node)

    while True:
        current_node = stack.get()
        current_node.state = State.BEEN_HERE
        curr_loc = current_node.location
        print(curr_loc)
        failures = 0
        for action in Direction:

            if BOARD_SIZE - 1 in curr_loc or 0 in curr_loc:
                invalid_actions = exits[get_border(curr_loc)]
            else:
                invalid_actions = tuple()

            if action == current_node.restore_action or action in invalid_actions:
                continue


            next_row = curr_loc.row + offsets[action][0]
            next_col = curr_loc.col + offsets[action][1]
            next_location = Location(next_row, next_col)

            candidate_cell = maze[next_location.row][next_location.col]

            if candidate_cell.state == State.UNKNOWN:
                stack._put(candidate_cell)
                prev_node = current_node
                feedback = yield action, candidate_cell

                if feedback == FB.KEEP_GOING:
                    failures = 0
                    current_node = candidate_cell
                    current_node.restore_action = opposites[action]  # how to go back
                    current_node.parent = prev_node


                else:
                    failures = failures + 1
                    if failures == 3:
                        current_node.state = State.DEAD_END
                        count = count + 1
                        # print(count, f'Dead end at {current_node.location} , going back!')
                        feedback = yield current_node.restore_action, current_node.parent
                        break

            else:
                # TODO: code duplication!!!
                failures = failures + 1
                if failures == 3:
                    current_node.state = State.DEAD_END
                    count = count + 1
                    # print(count, f'Dead end at {current_node.location} , going back!')
                    feedback = yield current_node.restore_action, current_node.parent


if __name__ == "__main__":

    with open('my_maze.txt', 'w') as m, open('maze_output.txt', 'w') as f:
        s = socket.socket()
        try:
            count = 0
            s.connect(('maze.csa-challenge.com', 80))
            start_time = time.time()
            for i in range(10):
                s.recv(1024)  # skip welcome messages
            pos = eval((s.recv(1024)[68:]).decode("utf-8"))  # tuple, starting point
            live_location = Location(BOARD_SIZE - 1 - pos[1], pos[0])  # First location
            f.write(f'Starting point is: {pos} which is {live_location} in the matrix')

            curr_node = maze[live_location.row][live_location.col]

            msg = s.recv(1024)  # skip 'What is your command?'

            solver = state_machine()  # got the closure inner
            next(solver)
            solver.send(curr_node)
            next_move, future_node = next(solver)  # get the first 'try' move
            s.send(str.encode(commands[next_move] + "\n"))

            while True:
                print('in main')
                msg = (s.recv(1024)).decode("utf-8")
                skip = (s.recv(1024)).decode("utf-8")  # skip  "> What is your command?"
                if skip != '> What is your command?\n':
                    f.write(skip)
                    print(skip)

                if msg[0] == '1' and len(msg) < 3:
                    curr_node = future_node
                    next_move, future_node = solver.send(FB.KEEP_GOING)
                    s.send(str.encode(commands[next_move] + "\n"))

                elif msg[0] == '0' and len(msg) < 3:
                    future_node.state = State.WALL
                    count = count + 1
                    # print(count, f'Wall at: {future_node.location}')
                    next_move, future_node = solver.send(FB.WALL)
                    s.send(str.encode(commands[next_move] + "\n"))
                else:
                    print(skip)
                    print(msg)
                    print(pos)
                    msg = (s.recv(1024)).decode("utf-8")
                    while msg != '':
                        print(msg)
                        msg = (s.recv(1024)).decode("utf-8")

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
