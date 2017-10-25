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

BLOCK_SIZE = 40   # pixels
ROWS = 12  # grid height
COLS = 5  # grid width

class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('maze')
        self.rows = ROWS
        self.cols = COLS
        self.block_size = BLOCK_SIZE
        self.height = self.rows * self.block_size
        self.width = self.cols * self.block_size
        self.geometry(str(self.width) + 'x' + str(self.height))
        #self.geometry('{}x{}'.format(self.width, self.height))
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white', height=self.height, width=self.width)
        #self.canvas = tk.Canvas(self, bg='white', height=10, width=100)

        # create vertical lines
        for c in range(self.cols):
            x0, y0, x1, y1 = c * self.block_size, 0, c * self.block_size, self.height 
            self.canvas.create_line(x0, y0, x1, y1)
        # create horizontal lines
        for r in range(self.rows):
            x0, y0, x1, y1 = 0, r * self.block_size, self.width, r * self.block_size
            self.canvas.create_line(x0, y0, x1, y1)

        # create origin
        origin = np.array([self.block_size // 2, self.block_size // 2])

        # pit
        pit1_center = origin + np.array([self.block_size * 2, self.block_size])
        self.pit1 = self.canvas.create_rectangle(
            pit1_center[0] - (self.block_size // 2), pit1_center[1] - (self.block_size // 2),
            pit1_center[0] + (self.block_size // 2), pit1_center[1] + (self.block_size // 2),
            fill='black')
        # pit
        pit2_center = origin + np.array([self.block_size, self.block_size * 2])
        self.pit2 = self.canvas.create_rectangle(
            pit2_center[0] - (self.block_size // 2), pit2_center[1] - (self.block_size // 2),
            pit2_center[0] + (self.block_size // 2), pit2_center[1] + (self.block_size // 2),
            fill='black')

        # create oval
        oval_center = origin + self.block_size * 2
        self.oval = self.canvas.create_oval(
            oval_center[0] - (self.block_size // 2), oval_center[1] - (self.block_size // 2),
            oval_center[0] + (self.block_size // 2), oval_center[1] + (self.block_size // 2),
            fill='yellow')

        # create red rect
        self.rect = self.canvas.create_rectangle(
            origin[0] - (self.block_size // 2), origin[1] - (self.block_size // 2),
            origin[0] + (self.block_size // 2), origin[1] + (self.block_size // 2),
            fill='red')

        # pack all
        self.canvas.pack()

    def reset(self):
        self.update()
        time.sleep(0.1)
        self.canvas.delete(self.rect)
        origin = np.array([(self.block_size // 2), (self.block_size // 2)])
        self.rect = self.canvas.create_rectangle(
            origin[0] - (self.block_size // 2), origin[1] - (self.block_size // 2),
            origin[0] + (self.block_size // 2), origin[1] + (self.block_size // 2),
            fill='red')
        # return observation
        return self.canvas.coords(self.rect)

    def step(self, action):
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > self.block_size:
                base_action[1] -= self.block_size
        elif action == 1:   # down
            if s[1] < (self.height - 1) * self.block_size:
                base_action[1] += self.block_size
        elif action == 2:   # right
            if s[0] < (self.width - 1) * self.block_size:
                base_action[0] += self.block_size
        elif action == 3:   # left
            if s[0] > self.block_size:
                base_action[0] -= self.block_size

        self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent

        s_ = self.canvas.coords(self.rect)  # next state

        # reward function
        if s_ == self.canvas.coords(self.oval):
            reward = 1
            done = True
        elif s_ in [self.canvas.coords(self.pit1), self.canvas.coords(self.pit2)]:
            reward = -1
            done = True
        else:
            reward = 0
            done = False

        return s_, reward, done

    def render(self):
        time.sleep(0.1)
        self.update()


def update():
    for t in range(10):
        s = maze.reset()
        while True:
            maze.render()
            a = 1
            s, r, done = maze.step(a)
            if done:
                break

if __name__ == '__main__':
    maze = Maze()
    maze.after(100, update)
    maze.mainloop()
