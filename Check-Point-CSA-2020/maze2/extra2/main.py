from __future__ import annotations
import socket
import time
import z3
import re
# from collections import namedtuple
from dataclasses import dataclass
# import numpy as np

from enum import Enum
from queue import LifoQueue
from typing import NamedTuple

BOARD_SIZE = 250  # Matrix
finished = False


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
    # failures_history: tuple  # for debugging the failures counters addition process


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
            Direction.LEFT: 'l', Direction.RIGHT: 'r',
            Special.INFORMATION: 'i', Special.LOCATION: 'c',
            Special.DISTANCE: 'g', Special.HELP: 'h',
            Special.SOLUTION: 's'}

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


# get the forbidden moves for each border location
def get_border(pos):
    MAX_VAL = BOARD_SIZE - 1
    MIN_VAL = 0
    row, col = pos
    print(f'checking border at', pos)
    if row == MIN_VAL:
        if col == MAX_VAL:
            return Borders.UPPER_RIGHT
        elif col == MIN_VAL:
            return Borders.UPPER_LEFT
        else:
            return Borders.UPPER

    elif row == MAX_VAL:
        if col == MAX_VAL:
            return Borders.BUTTOM_RIGHT
        elif col == MIN_VAL:
            return Borders.BUTTOM_LEFT
        else:
            return Borders.BUTTOM

    else:
        if col == MIN_VAL:
            return Borders.LEFT
        else:
            return Borders.RIGHT


def get_forbidden_moves(curr_loc):
    if BOARD_SIZE - 1 in curr_loc or 0 in curr_loc:
        invalid_actions = exits[get_border(curr_loc)]
    else:
        invalid_actions = tuple()

    return invalid_actions


def state_machine():
    global maze
    global finished
    current_node = yield
    count = 0  # number of marked cells in the maze
    stack = LifoQueue()
    stack._put(Special.INFORMATION)
    start_point = current_node.location
    curr_loc = start_point
    u = z3.Int('u')
    v = z3.Int('v')
    z3solver = z3.Solver()
    equations_cnt = 0

    while not stack.empty():
        # print(f'stack-size: {stack._qsize()} {count} ', end='')
        current_action = stack._get()
        # print(current_action)
        current_node.state = State.MARKED
        feedback = yield current_action
        # print('3', end='')
        dont_send_info_command = False

        if current_action == Special.INFORMATION:
            count = count + 1
            print(count,end='|')
            if count % 10 == 0:
                print('')

            invalid_actions = get_forbidden_moves(curr_loc)

            for direction in Direction:
                if commands[direction] not in feedback and direction not in invalid_actions:
                    wall_cell = get_next_cell(curr_loc, direction)
                    wall_cell.state = State.MARKED

            for move in feedback:
                if get_key(move) in invalid_actions or get_key(move) == current_node.restore_action:
                    continue

                direction = get_key(move)
                open_cell = get_next_cell(curr_loc, direction)
                if open_cell.state == State.NOT_MARKED:
                    open_cell.parent = current_node
                    open_cell.restore_action = opposites[direction]
                    current_node.options += 1
                    stack._put(Special.INFORMATION)
                    stack._put(Special.DISTANCE)
                    stack._put(direction)

        elif current_action == Special.DISTANCE:
            if feedback == FB.FAR_FAR_AWAY:
                continue
            else:
                print('feedback is', feedback, end='')
                print(f'#equations: {equations_cnt}')
                # if count > 4000 and feedback < 40:
                # if count > 4000:
                equations_cnt += 1
                x, y = BOARD_SIZE - 1 - curr_loc[1], curr_loc[0]
                z3solver.add(u ** 2 - 2 * u * x + x ** 2 + v ** 2 - 2 * v * y + y ** 2 == feedback)
                if equations_cnt > 1000:
                    if z3solver.check() == z3.sat:
                        model = z3solver.model()
                        res = f'({model[u]},{model[v]})'
                        finished = True
                        stack._put(res)

                continue

        elif feedback == FB.KEEP_GOING:
            current_node = get_next_cell(curr_loc, current_action)
            curr_loc = current_node.location
            # if stack._qsize() > 1:
            #     temp = stack._get()
            #     if temp == Special.INFORMATION:
            #         marked_around_me = 0
            #         invalid_actions = get_forbidden_moves(curr_loc)
            #         for direction in Direction:
            #             if direction in invalid_actions:
            #                 continue
            #             else:
            #                 checked_neighbour = get_next_cell(curr_loc, direction)
            #                 if checked_neighbour.state == State.MARKED:
            #                     marked_around_me += 1
            #         if marked_around_me == 4 - len(invalid_actions):
            #             dont_send_info_command = True
            #         else:
            #             stack._put(temp)
            #     else:
            #         stack._put(temp)


        elif feedback == FB.WALL:
            print('NOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
            current_node.options -= 1
            current_node.failures +=1
        elif feedback == FB.FINISH_HIM:
            print('special feeback!: ', feedback)
            stack._put(Special.SOLUTION)
            continue
        else:
            print('bad feedback:', feedback)

        cond_b = (current_action == Special.INFORMATION) and (current_node.options == 0) and count > 1
        cond_c = (current_node.failures > 0) and (current_node.failures == current_node.options)
        # if dont_send_info_command or cond_b or cond_c:
        if cond_b or cond_c:
            if current_node.parent is None:
            # print(dont_send_info_command)
                print(equations_cnt)
                print(current_action)
                print('how can it be:? ', current_node)
            current_node.parent.failures += 1
            print('.', end='')
            stack._put(current_node.restore_action)


def finish_move(sock, solution=None):
    if solution == None:
        sock.send(str.encode(commands[Special.LOCATION] + "\n"))
        solution = (sock.recv(1024)).decode("utf-8")
        print(solution)
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        msg = (sock.recv(1024)).decode("utf-8").rstrip()
        print(msg)

    sock.send(str.encode(commands[Special.SOLUTION] + "\n"))
    msg = (sock.recv(1024)).decode("utf-8").rstrip()
    print(msg)
    print('---------------------------')

    sock.send(str.encode(solution + '\n'))
    msg = (sock.recv(1024)).decode("utf-8")
    print(msg)
    print('ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ')
    msg = ''
    while (msg != '' and msg != '\n'):
        msg = (sock.recv(1024)).decode("utf-8").rstrip()
        print(msg)
    print('---------------------------')
    return


if __name__ == "__main__":

    INFO_LEN = len('l=0, r=1, u=0, d=0\n')
    sock = socket.socket()
    sock.settimeout(60)
    try:
        sock.connect(('maze.csa-challenge.com', 80))
        start_time = time.time()
        for i in range(10):
            sock.recv(1024)  # skip welcome messages

        pos = eval((sock.recv(1024).decode("utf-8")[68:]))  # tuple, starting point
        live_location = Location(BOARD_SIZE - 1 - pos[0], pos[1])
        print(f'Starting point is: {pos} which is {live_location} in the matrix')
        first_node = maze[live_location.row][live_location.col]

        solver = state_machine()  # got the closure inner
        next(solver)
        next_move = solver.send(first_node)  # get the first 'try' move

        while True:
            skip = (sock.recv(1024)).decode("utf-8").rstrip()  # skip  "> What is your command?"
            if skip.find('> What is your command?') == -1:
                print('unique message:', skip)
            # print(next_move)
            if not finished:
                sock.send(str.encode(commands[next_move] + "\n"))
            else:
                print("FINISHEDDDD")

            if next_move == Special.INFORMATION:
                msg = (sock.recv(INFO_LEN)).decode("utf-8")
                if len(msg) < 4:
                    print(msg)
                    finish_move(sock)
                elif msg[0] == 'l' and msg[1] == '=':
                    msg = msg.rstrip().replace(' ', '')
                    msg = msg.split(',')
                    options = [d[0] for d in msg if d[-1] == '1']
                    next_move = solver.send(options)
            else:
                if isinstance(next_move, Direction):
                    msg = (sock.recv(2)).decode("utf-8").rstrip()
                    if msg[0] == '1':
                        # print('B', end='')
                        next_move = solver.send(FB.KEEP_GOING)
                        # print('b', end='')
                    else:
                        print(next_move)
                        print(msg)
                        print('OOOPSSSSSSSSSSSSSSSSSSSS')
                        next_move = solver.send(FB.WALL)


                else:
                    msg = (sock.recv(1024)).decode("utf-8").rstrip()
                    if msg.find('far far away') != -1:
                        # print('C', end='')
                        next_move = solver.send(FB.FAR_FAR_AWAY)
                        # print('c', end='')
                    elif msg.find('Your distance from the treasure is') != -1:
                        print(msg)
                        dist = int(re.search(r'\d+', msg).group())
                        next_move = solver.send(dist)
                        if isinstance(next_move, str) and len(next_move) > 3 and next_move[0] == '(':
                            finish_move(sock, next_move)

                    elif msg == '> What is your command?\n':
                        print('Got what is your command')
                        continue
                    else:
                        print(next_move)
                        print('Unique:', msg, 'Should be - what is your command')
                        print('******************')
                        # next_move = solver.send(FB.FINISH_HIM)
                        finish_move(sock)

                        break

        print("--- %s seconds ---" % (time.time() - start_time))

    except ValueError:
        pass
    finally:
        sock.close()
        game_over = True
