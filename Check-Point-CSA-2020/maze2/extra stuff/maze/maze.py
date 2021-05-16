import socket
import time
import operator
import numpy as np
from enum import Enum

BOARD_SIZE = 250

UNKNOWN = '.'
BEEN_HERE = 'X'
WALL = '='
START = 'S'


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

# right hand rule
now_what = {Action.UP: (Action.RIGHT, Action.UP, Action.LEFT, Action.DOWN),
            Action.DOWN: (Action.LEFT, Action.DOWN, Action.RIGHT, Action.UP),
            Action.LEFT: (Action.UP, Action.LEFT, Action.DOWN, Action.RIGHT),
            Action.RIGHT: (Action.DOWN, Action.RIGHT, Action.UP, Action.LEFT)}

exits = {Borders.UPPER: (Action.UP,),
         Borders.BUTTOM: (Action.DOWN,),
         Borders.LEFT: (Action.LEFT,),
         Borders.RIGHT: (Action.RIGHT,),
         Borders.UPPER_LEFT: (Action.LEFT, Action.UP),
         Borders.BUTTOM_LEFT: (Action.LEFT, Action.DOWN),
         Borders.UPPER_RIGHT: (Action.RIGHT, Action.UP),
         Borders.BUTTOM_RIGHT: (Action.RIGHT, Action.DOWN)}


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
    failures = 0

    # make the first succesful move
    trial_action = None
    feedback = None
    for act in Action:
        feedback, input_pos, input_cube = yield act
        if feedback == Feedback.KEEP_GOING:
            trial_action = act
            break

    while True:

        if feedback == Feedback.WALL:
            failures = failures + 1

        elif feedback == Feedback.KEEP_GOING:
            failures = 0
            last_successful_action = trial_action
            next_actions = now_what[last_successful_action]

            if BOARD_SIZE - 1 in input_pos or 0 in input_pos:
                invalid_actions = exits[get_border(input_pos)]
                next_actions = (e for e in next_actions if e not in invalid_actions)


        trial_action = next_actions[failures]
        dx, dy = offsets[trial_action]
        dy = -dy
        cube_pos = tuple(map(operator.add, ((1, 1)), ((dy, dx))))
        if input_cube[cube_pos[0], cube_pos[1]] != WALL:
            feedback, input_pos, input_cube = yield trial_action
        else:
            feedback = Feedback.WALL


if __name__ == "__main__":
    game_over = False

    with open('my_maze.txt', 'w') as m, open('maze_output.txt', 'w') as f:
        while not game_over:
            # maze = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=np.int8)
            maze = np.full((BOARD_SIZE + 2, BOARD_SIZE + 2), UNKNOWN)
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

                maze[BOARD_SIZE - pos[1], pos[0] + 1] = START  # starting point

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

                        row = BOARD_SIZE - pos[1]
                        col = pos[0] + 1
                        cube = maze[row - 1:row + 2, col - 1:col + 2]

                        curr_move = solver.send(tuple((Feedback.KEEP_GOING, pos, cube)))
                        s.send(str.encode(commands[curr_move] + "\n"))

                    elif msg[0] == '0' and len(msg) < 3:
                        maze[BOARD_SIZE - future_pos[1], future_pos[0] + 1] = WALL
                        row = BOARD_SIZE - pos[1]
                        col = pos[0] + 1
                        cube = maze[row - 1:row + 2, col - 1:col + 2]
                        curr_move = solver.send(tuple((Feedback.WALL, pos, cube)))
                        s.send(str.encode(commands[curr_move] + "\n"))
                    else:
                        print(skip)
                        print(msg)

                        print(pos)
                        print(cube)

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

                maze_as_list = maze.tolist()
                for line in maze_as_list:
                    m.write(''.join(line) + '\n')

                s.close()
                game_over = True
