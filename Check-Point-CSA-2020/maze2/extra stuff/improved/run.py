import socket
import time
import operator
import os
import numpy as np
# from itertools import chain
from enum import Enum
# from pprint import pprint

BOARD_SIZE = 250


class Feedback(Enum):
    KEEP_GOING = 1
    WALL = 2


class Action(Enum):
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4


class Borders(Enum):
    UPPER = 1
    BUTTOM = 2
    LEFT = 3
    RIGHT = 4
    UPPER_LEFT = 5
    UPPER_RIGHT = 6
    BUTTOM_LEFT = 7
    BUTTOM_RIGHT = 8


commands = {Action.UP: 'u', Action.DOWN: 'd',
            Action.LEFT: 'l', Action.RIGHT: 'r'}

offsets = {Action.UP: (0, 1), Action.DOWN: (0, -1),
           Action.LEFT: (-1, 0), Action.RIGHT: (1, 0)}

now_what = {Action.UP: (Action.RIGHT, Action.UP, Action.LEFT, Action.DOWN),
            Action.DOWN: (Action.LEFT, Action.DOWN, Action.RIGHT, Action.UP),
            Action.LEFT: (Action.UP, Action.LEFT, Action.DOWN, Action.RIGHT),
            Action.RIGHT: (Action.DOWN, Action.RIGHT, Action.UP, Action.LEFT)}

exits = {Borders.UPPER:       (Action.UP,),
         Borders.BUTTOM:      (Action.DOWN,),
         Borders.LEFT:        (Action.LEFT,),
         Borders.RIGHT:        (Action.RIGHT,),
         Borders.UPPER_LEFT:  (Action.LEFT, Action.UP),
         Borders.BUTTOM_LEFT: (Action.LEFT, Action.DOWN),
         Borders.UPPER_RIGHT:  (Action.RIGHT, Action.UP),
         Borders.BUTTOM_RIGHT:  (Action.RIGHT, Action.DOWN)}


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

    pos = yield  # get the starting position
    failures = 0

    # make the first succesful move
    for last_successful_move in Action:
        feedback, pos, cube = yield last_successful_move
        if (feedback == Feedback.KEEP_GOING):
            break

    next_actions = now_what[last_successful_move]

    while True:
        feedback == Feedback.WALL
        failures = 0

        while feedback == Feedback.WALL:
            trial_action = next_actions[failures]
            dx, dy = offsets[trial_action]
            dy = -dy
            cube_pos = tuple(map(operator.add, ((1, 1)), ((dy, dx))))
            print(cube_pos)
            if cube[cube_pos[0], cube_pos[1]] != 3:
                break
            else:
                failures = failures+1

            feedback, pos, cube = yield trial_action

            if pos[0] < 0 or pos[1] < 0 or pos[0] > BOARD_SIZE or pos[1] > pos[0] > BOARD_SIZE:
                print('NOOOOTTTTTTTTT GOOOD - ALERT!')

            if feedback == Feedback.KEEP_GOING:
                last_successful_move = trial_action

                if BOARD_SIZE-1 in pos or 0 in pos:
                    next_actions = now_what[last_successful_move]
                    priority_actions = exits[get_border(pos)]
                    next_actions = (*priority_actions, *next_actions)

                else:
                    next_actions = now_what[last_successful_move]


if __name__ == "__main__":
    game_over = False

    with open('my_maze.txt', 'w') as m, open('maze_output.txt', 'w') as f:
        while not game_over:
            maze = np.zeros(((BOARD_SIZE+1, BOARD_SIZE+1)), dtype=np.int8)
            s = socket.socket()

            try:
                count = 0
                port = 80
                s.connect(('maze.csa-challenge.com', port))

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

                maze[BOARD_SIZE - 1 - pos[1], pos[0]] = 1

                s.send(str.encode(commands[curr_move] + "\n"))

                while True:

                    msg = (s.recv(1024)).decode("utf-8")
                    # skip the "> What is your command?"
                    skip = (s.recv(1024)).decode("utf-8")
                    if skip != '> What is your command?\n':
                        f.write(skip)
                        print(skip)

                    future_pos = tuple(
                        map(operator.add, pos, offsets[curr_move]))
                    if (msg[0] == '1' and len(msg) < 3):

                        pos = future_pos
                        if maze[BOARD_SIZE - 1 - pos[1], pos[0]] == 0:
                            maze[BOARD_SIZE - 1 - pos[1]][pos[0]] = 2
                            count = count + 1
                            print(count)
                            if count > 950:
                                raise ValueError('Hi')

                        row = BOARD_SIZE - 1 - pos[1]
                        col = pos[0]
                        cube = maze[row-1:row+2, col-1:col+2]
                        curr_move = solver.send(
                            tuple((Feedback.KEEP_GOING, pos, cube)))
                        s.send(str.encode(commands[curr_move] + "\n"))

                    elif (msg[0] == '0' and len(msg) < 3):
                        maze[BOARD_SIZE - 1 - future_pos[1], future_pos[0]] = 3
                        row = BOARD_SIZE - 1 - pos[1]
                        col = pos[0]
                        cube = maze[row-1:row+2, col-1:col+2]
                        curr_move = solver.send(
                            tuple((Feedback.WALL, pos, cube)))
                        s.send(str.encode(commands[curr_move] + "\n"))
                    else:

                        print(skip)
                        print(msg)

                        msg = (s.recv(1024)).decode("utf-8")
                        while (msg != ''):
                            print(msg)
                            msg = (s.recv(1024)).decode("utf-8")

                        game_over = True

                        for line in maze:
                            m.write(''.join(line))
                            m.write('\n')

                        break

                f.write("--- %s seconds ---" % (time.time() - start_time))

            except ValueError:
                pass
            finally:
                s.close()
