import socket
import time
import operator
# import os
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

now_what = {Action.UP: (Action.LEFT, Action.UP, Action.RIGHT, Action.DOWN),
            Action.DOWN: (Action.RIGHT, Action.DOWN, Action.LEFT, Action.UP),
            Action.LEFT: (Action.DOWN, Action.LEFT, Action.UP, Action.RIGHT),
            Action.RIGHT: (Action.UP, Action.RIGHT, Action.DOWN, Action.LEFT)}

exits = {Borders.UPPER:       (Action.UP,),
         Borders.BUTTOM:      (Action.DOWN,),
         Borders.LEFT:        (Action.LEFT,),
         Borders.RIGHT:        (Action.RIGHT,),
         Borders.UPPER_LEFT:  (Action.LEFT, Action.UP),
         Borders.BUTTOM_LEFT: (Action.LEFT, Action.DOWN),
         Borders.UPPER_RIGHT:  (Action.RIGHT, Action.UP),
         Borders.BUTTOM_RIGHT:  (Action.RIGHT, Action.DOWN)}

maze = [['e'] * (BOARD_SIZE+1) for i in range(BOARD_SIZE+1)]

s = socket.socket()

# on_border = False


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
    global maze
    global on_border

    pos = yield  # get the starting position
    failures = 0

    # make the first succesful move
    for last_successful_move in Action:
        feedback, pos = yield last_successful_move
        if (feedback == Feedback.KEEP_GOING):
            break

    next_actions = now_what[last_successful_move]

    # print(f'fb={feedback}', f'pos= {pos}',
    #       f'last_successful_move={last_successful_move}')

    while True:
        trial_action = next_actions[failures]
        feedback, pos = yield trial_action
        # print(pos)
        if pos[0] < 0 or pos[1] < 0 or pos[0] > BOARD_SIZE or pos[1] > pos[0] > BOARD_SIZE:
            print('NOOOOTTTTTTTTT GOOOD - ALERT!')
        if feedback == Feedback.KEEP_GOING:
            # print(pos)
            last_successful_move = trial_action
            # print(f'fb={feedback}', f'pos= {pos}',
            #       f'last_successful_move={last_successful_move}')

            failures = 0
            if BOARD_SIZE-1 in pos or 0 in pos and maze[BOARD_SIZE - 1 - pos[1]][pos[0]] != 'X':
                next_actions = now_what[last_successful_move]
                priority_actions = exits[get_border(pos)]
                next_actions = (*priority_actions, *next_actions)

            else:
                # on_border = False
                next_actions = now_what[last_successful_move]

        elif feedback == Feedback.WALL:
            failures = failures + 1
            if failures == 5:
                print(f'5 failures at {pos}')
            elif failures == 6:
                print(f'6 failures at {pos}')
            # print(f'failures={failures}')


if __name__ == "__main__":

    with open('my_maze.txt', 'w') as m, open('maze_output.txt', 'w') as f:
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

            maze[BOARD_SIZE - 1 - pos[1]][pos[0]] = 'S'

            # next(solver)
            # print(f'first move was {curr_move}')
            s.send(str.encode(commands[curr_move] + "\n"))

            while True:

                msg = (s.recv(1024)).decode("utf-8")
                # skip the "> What is your command?"
                skip = (s.recv(1024)).decode("utf-8")
                if skip != '> What is your command?\n':
                    f.write(skip)

                future_pos = tuple(
                    map(operator.add, pos, offsets[curr_move]))
                if (msg[0] == '1' and len(msg) < 3):
                    # actually we use the previous move
                    pos = future_pos
                    if maze[BOARD_SIZE - 1 - pos[1]][pos[0]] == 'e':
                        maze[BOARD_SIZE - 1 - pos[1]][pos[0]] = 'X'
                        count = count + 1
                        print(count)
                        f.write(count, '\n')
                        if count > 20000:
                            m.seek(os.SEEK_SET)
                            for line in maze:
                                m.write(''.join(line))
                                m.write('\n')
                    curr_move = solver.send(
                        tuple((Feedback.KEEP_GOING, pos)))

                elif (msg[0] == '0' and len(msg) < 3):
                    # if not on_border:
                    maze[BOARD_SIZE - 1 - future_pos[1]][future_pos[0]] = 'W'
                    curr_move = solver.send(tuple((Feedback.WALL, pos)))
                else:
                    m.seek(os.SEEK_SET)
                    for line in maze:
                        m.write(''.join(line))
                        m.write('\n')

                    print(skip)
                    print(msg)
                    msg = (s.recv(1024)).decode("utf-8")
                    while (msg != ''):
                        print(msg)
                        msg = (s.recv(1024)).decode("utf-8")
                    break

                # f.write(msg)
                # f.write(skip)

                # print(f'curr_move was {curr_move}')
                s.send(str.encode(commands[curr_move] + "\n"))

            f.write("--- %s seconds ---" % (time.time() - start_time))

        except:
            raise
        finally:
            s.close()
