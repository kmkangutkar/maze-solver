"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       pits       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the environment part of this example. The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""

import numpy as np
import time
import sys
import tkinter as tk
import random

BLOCK_SIZE = 40   # pixels
ACTION_SPACE = ['up', 'down', 'left', 'right']
'''
ROWS = 4  # grid height
COLS = 4  # grid width
'''

class MazeWithoutGui():
    def __init__(self, filename='example_maze'):
        self.action_space = ACTION_SPACE
        self.n_actions = len(self.action_space)

        self.rows = None
        self.cols = None
        self.maze_lines = None
        self._read_maze(filename)

        self.pits = []
        self.open_blocks = []
        self._populate_blocks(self.maze_lines) 
        self.goal = self._accept_goal()
        self.start = None

    def _read_maze(self, filename):
        with open(filename) as f:
            self.rows, self.cols = [int(x) for x in f.readline().strip().split()]
            self.maze_lines = [line.strip().split() for line in f.readlines()]
        print(self.rows, self.cols)

    def _accept_goal(self, filename='goal_coordinates'):
        with open(filename) as f:
             col, row = [int(x) for x in f.readline().strip().split()]
        goal = (col, row)
        return goal 

    def _populate_blocks(self, lines):
        for row, line in enumerate(lines):
            for col, elem in enumerate(line):
                position = col, row
                if elem == 'P':
                    self.pits.append(position)
                else:
                    self.open_blocks.append(position)
        print('pits:', self.pits)
        print('open:', self.open_blocks)

    def reset(self):
        #random start state
        #self.start = random.choice(self.open_blocks)

        #fixed start state
        self.start = (0, 0)

        return self.start

    def step(self, action):
        x, y = self.start[:2]
        base_action = [x, y]
        if action == 0 and y > 0:   # up
            base_action[1] -= 1
        elif action == 1 and y < (self.rows - 1):   # down
            base_action[1] += 1
        elif action == 2 and x < (self.cols - 1):   # right
            base_action[0] += 1
        elif action == 3 and x > 0:   # left
            base_action[0] -= 1

        self.start = tuple(base_action) 

        new_state = self.start  # next state

        # reward function
        if new_state == self.goal:
            reward = 1
            done = True
        elif new_state in self.pits:
            reward = -1
            done = True
        else:
            reward = 0
            done = False

        return new_state, reward, done


class Maze(tk.Tk, object):
    def __init__(self, filename='example_maze'):
        super(Maze, self).__init__()

        # constants
        self.action_space = ACTION_SPACE
        self.n_actions = len(self.action_space)
        self.block_size = BLOCK_SIZE
        #self.title('maze') # rename later as dense or sparse with loops

        self.rows = None
        self.cols = None
        self._read_maze(filename)

        self.height = self.rows * self.block_size
        self.width = self.cols * self.block_size
        self.geometry(str(self.width) + 'x' + str(self.height))

        self.canvas = None
        self.pits = []
        self.open_blocks = []
        self._build_maze()

        self.goal = self._accept_goal()
        self.start = None
        '''
        self._rl_learn() 

        self.start = None
        self._accept_start()
        '''
       

    def _read_maze(self, filename):
        with open(filename) as f:
            self.rows, self.cols = [int(x) for x in f.readline().strip().split()]
            self.maze_lines = [line.strip().split() for line in f.readlines()]
        print(self.rows, self.cols)


    def _populate_blocks(self, lines):
        #self.pits = [[self.create_object(elem, col, row) for col, elem in enumerate(line)] for row, line in enumerate(lines)]
        for row, line in enumerate(lines):
            for col, elem in enumerate(line):
                if elem == 'P':
                    created_object = self.create_object(elem, col, row)
                    self.pits.append(created_object)
                else:
                    self.open_blocks.append((col, row))


    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white', height=self.height, width=self.width)

        # create vertical lines
        for c in range(self.cols):
            x0, y0, x1, y1 = c, 0, c, self.rows
            self.create_line(x0, y0, x1, y1)
        # create horizontal lines
        for r in range(self.rows):
            x0, y0, x1, y1 = 0, r, 0, self.cols
            self.create_line(x0, y0, x1, y1)

        self._populate_blocks(self.maze_lines)

        # pack all
        self.canvas.pack()

    def _accept_goal(self, filename='goal_coordinates'):
        with open(filename) as f:
            col, row = np.array([int(x) for x in f.readline().strip().split()])
        goal = self.create_object('G', col, row)
        return goal

    def _accept_start(self, filename='start_coordinates'):
        with open(filename) as f:
            row, col = np.array([int(x) for x in f.readline()])
        start = self.create_object('S', col, row)
        return start

    def reset(self):
        self.update()
        time.sleep(0.1)
        self.canvas.delete(self.start)

        #random start state
        '''
        start_position = random.choice(self.open_blocks)
        print(start_col, start_row)
        '''

        #fixed start state
        start_position = (0, 0)

        top_left_corner = self.block_size * np.array(start_position)
        created_object = self.create_object('S', *top_left_corner)
        self.start = created_object

        # return observation
        return start_position

    def step(self, action):
        s = self.canvas.coords(self.start)
        x, y = s[:2]
        base_action = np.array([0, 0])
        if action == 0:   # up
            if y > 0:
                base_action[1] -= self.block_size
        elif action == 1:   # down
            if y < (self.rows - 1) * self.block_size:
                base_action[1] += self.block_size
        elif action == 2:   # right
            if x < (self.cols - 1) * self.block_size:
                base_action[0] += self.block_size
        elif action == 3:   # left
            if x > 0:
                base_action[0] -= self.block_size

        self.canvas.move(self.start, base_action[0], base_action[1])  # move agent

        s_ = self.canvas.coords(self.start)  # next state

        # reward function
        if s_ == self.canvas.coords(self.goal):
            reward = 1
            done = True
        elif s_ in [self.canvas.coords(p) for p in self.pits]:
            reward = -1
            done = True
        else:
            reward = 0
            done = False

        return s_, reward, done

    def render(self):
        time.sleep(0.1)
        self.update()

    def create_object(self, object_label, col, row):
        creation_functions = {
            'P':self.canvas.create_rectangle,
            'S':self.canvas.create_oval,
            'G':self.canvas.create_oval,
        }
        colors = {
            'P':'black',
            'S':'red',
            'G':'green',
        }

        object_top_left_corner = self.block_size * np.array([col, row])
        other_corner = object_top_left_corner + self.block_size * np.array([1, 1])
        created_object = creation_functions[object_label](*object_top_left_corner, *other_corner, fill=colors[object_label])

        return created_object
    
    def create_line(self, x0, y0, x1, y1):
        x0, y0, x1, y1 = tuple(self.block_size * np.array([x0, y0, x1, y1]))
        self.canvas.create_line(x0, y0, x1, y1)

def update():
    for t in range(10):
        s = maze.reset()
        while True:
            #maze.render()
            a = 1
            s, r, done = maze.step(a)
            if done:
                break

if __name__ == '__main__':
    maze = Maze()
    maze.after(100, update)
    maze.mainloop()
