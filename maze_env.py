from parameters import BLOCK_SIZE, START, GOAL, MOVEMENT_REWARD, GOAL_REWARD, PIT_REWARD, MAZE_FILE, ACTION_SPACE

import numpy as np
import time
import sys
import tkinter as tk
import random

class Maze():
    def __init__(self, filename=MAZE_FILE):
        self.action_space = ACTION_SPACE
        self.n_actions = len(self.action_space)

        self.cols = None
        self.rows = None
        self.maze_lines = None
        self._read_maze(filename)

        self.pit_locations = []
        self.open_locations = []
        self._populate_blocks(self.maze_lines) 
        self.goal_coordinates = GOAL
        self.start_coordinates = START

    def _read_maze(self, filename):
        with open(filename) as f:
            self.cols, self.rows = [int(x) for x in f.readline().strip().split()]
            self.maze_lines = [line.strip() for line in f.readlines()]
        print(self.cols, self.rows)

    def _populate_blocks(self, lines):
        for row, line in enumerate(lines):
            for col, elem in enumerate(line):
                position = col, row
                if elem == 'P':
                    self.pit_locations.append(position)
                else:
                    self.open_locations.append(position)
        print('pit locations:', self.pit_locations)
        print('open:', self.open_locations)

    def reset(self):
        #random start state
        #self.start_coordinates = random.choice(self.open_locations)

        #fixed start state
        self.start_coordinates = START

        return self.start_coordinates

    def step(self, action):
        x, y = self.start_coordinates
        base_action = [x, y]
        if action == 0 and y > 0:   # up
            base_action[1] -= 1
        elif action == 1 and y < (self.rows - 1):   # down
            base_action[1] += 1
        elif action == 2 and x < (self.cols - 1):   # right
            base_action[0] += 1
        elif action == 3 and x > 0:   # left
            base_action[0] -= 1

        new_state = tuple(base_action)

        # reward function
        if new_state == self.goal_coordinates:
            reward = GOAL_REWARD
            done = True
        elif new_state in self.pit_locations:
            reward = PIT_REWARD
            done = True
            #done = False
            #new_state = self.start_coordinates # reset new_state to old state
        else:
            reward = MOVEMENT_REWARD
            done = False

        self.start_coordinates = new_state
        return new_state, reward, done

class MazeWithGui(Maze, tk.Tk):
    def __init__(self, filename=MAZE_FILE):
        Maze.__init__(self)
        tk.Tk.__init__(self)

        # constants
        self.block_size = BLOCK_SIZE
        self.title('maze') # rename later as dense or sparse with loops

        self.height = self.rows * self.block_size
        self.width = self.cols * self.block_size
        self.geometry(str(self.width) + 'x' + str(self.height))


        self.canvas = None
        self.pit_objects = []
        self._build_maze()

        self.goal_object = self.create_object('G', *GOAL)
        self.start_object = self.create_object('S', *START)

    def _create_pit_objects(self):
        for location in self.pit_locations:
            created_object = self.create_object('P', *location)
            self.pit_objects.append(created_object)

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white', height=self.height, width=self.width)

        # create vertical lines
        for c in range(self.cols):
            x0, y0, x1, y1 = c, 0, c, self.rows
            self.create_line(x0, y0, x1, y1)
        # create horizontal lines
        for r in range(self.rows):
            x0, y0, x1, y1 = 0, r, self.cols, r
            self.create_line(x0, y0, x1, y1)

        self._create_pit_objects()

        # pack all
        self.canvas.pack()

    def reset(self):
        self.update()
        time.sleep(0.1)
        self.canvas.delete(self.start_object)
        start_position = Maze.reset(self)
        top_left_corner = self.block_size * np.array(start_position)
        self.start_object = self.create_object('S', *top_left_corner)

        # return observation
        return start_position

    def step(self, action):
        s = self.canvas.coords(self.start_object)
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

        self.canvas.move(self.start_object, *base_action)  # move agent

        new_state = self.canvas.coords(self.start_object)  # next state

        # reward function
        if new_state == self.canvas.coords(self.goal_object):
            reward = GOAL_REWARD
            done = True
        elif new_state in [self.canvas.coords(p) for p in self.pit_objects]:
            reward = PIT_REWARD
            done = True
            #done = False
            #base_action = x, y # reset new_state to old state
        else:
           reward = MOVEMENT_REWARD
           done = False

        #self.canvas.move(self.start_object, *base_action)  # move agent

        '''
        new_state, reward, done = Maze.step(self, action)
        base_action = self.block_size * np.array(new_state)
        self.canvas.move(self.start_object, *base_action)  # move agent
        '''
        return new_state, reward, done

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
