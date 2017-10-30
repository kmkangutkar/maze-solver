from itertools import combinations
from parameters import N_COLS, N_ROWS

import numpy as np
import random
import operator

class Builder():
    actions = {
        'left': (0, -1),
        'up': (-1, 0),
        'right': (0, +1),
        'down': (+1, 0),
    }
    circular_directions = ('left', 'up', 'right', 'down')

    def __init__(self, col, row, direction, max_distance, label):
        self.position = (col, row)
        self.direction = direction
        self.max_distance = max_distance
        self.remaining_distance = random.randint(1, self.max_distance)
        self.id = label

    def move(self):
        self.position = self.check_move()
        self.remaining_distance -= 1

    def check_move(self):
        change = Builder.actions[self.direction]
        new_position = tuple(map(operator.add, self.position, change))
        return new_position

    def turn_randomly(self):
        curr_direction_index = Builder.circular_directions.index(self.direction)
        new_direction_index = curr_direction_index + random.choice([-1, +1])
        self.direction = Builder.circular_directions[new_direction_index % len(Builder.circular_directions)]

    def choose_distance_randomly(self):
        self.remaining_distance = random.randint(1, self.max_distance)

    def start_new_path(self):
        self.turn_randomly()
        self.choose_distance_randomly()

    def is_hit_wall(self, n_cols, n_rows):
        temp_position = self.check_move()
        safe = 0 <= temp_position[0] < n_cols and 0 <= temp_position[1] < n_rows
        hit_wall = not safe
        return hit_wall


def read_dimensions():
    n_cols = N_COLS
    n_rows = N_ROWS
    return n_cols, n_rows

def generate_builders(n_cols, n_rows, packing_fraction=0.01, max_distance_ratio=0.5):
    maze_area = n_cols * n_rows
    builder_max_distance = int(max_distance_ratio * min(n_cols, n_rows))
    n_start_positions = max(1, int(packing_fraction * maze_area))
    start_positions = []
    builders = []
    while len(start_positions) < n_start_positions:
        new_position = (random.randint(0, n_cols - 1), random.randint(0, n_rows - 1))
        if new_position in start_positions:
            continue
        start_positions.append(new_position)
        
        directions = Builder.circular_directions
        n_builders = random.randint(1, len(directions))
        possible_combinations = list(combinations(directions, n_builders))
        for d in random.choice(possible_combinations):
            b = Builder(*new_position, d, builder_max_distance, len(start_positions))
            builders.append(b)
        print(len(start_positions), n_start_positions, len(builders))
    return builders, start_positions

def print_maze(maze):
    OPEN = '.'#0
    PIT = 'P'#1
    n_cols, n_rows = maze.shape
    with open('tmp/example_maze', 'w') as f:
        print(n_cols, n_rows)
        print(n_cols, n_rows, file=f)
        for r in range(n_rows):
            for c in range(n_cols):
                if maze[c][r] > 0:
                    symbol = OPEN
                else:
                    symbol = PIT
                print(symbol, end='')
                print(symbol, end='', file=f)
            print()
            print(file=f)

'''
# The following is an attempt to reduce the width of all paths in the maze to 1.
# We plan to do this by removing builders which come adjacent to paths of labels
# which match builders of other starting points.

def is_hit_other_path_extra(maze, b):
    n_rows, n_cols = maze.shape
    adjacent_squares = []
    for change in Builder.actions.values():
        new_position = tuple(map(operator.add, b.position, change))
        adjacent_squares.append(new_position)

    safe = all(0 <= pos[0] < n_cols and 0 <= pos[1] < n_rows and maze[pos] in [0, b.id] for pos in adjacent_squares)
    hit_other_path = not safe
    return hit_other_path
'''

def is_hit_other_path(maze, b):
    safe = maze[b.position] in [0, b.id]
    hit_other_path = not safe
    return hit_other_path

def main():
    '''
    take input: cols, rows
    make a list of the start positions for the builders
    for each start position:
        generate 1 to 4 builders starting at this position and going in different directions
        assign random distance to each builder
    while there are builders:
        for b in builders:
            move 1 space and decrement remaining distance
            if hit other builder's path:
                builder die
            if hit wall or distance over:
                turn left or right
                new random distance
    write maze to file while replacing 1 with Pit and 0 with Open
    '''

    n_cols, n_rows = read_dimensions()
    maze = np.zeros((n_cols, n_rows), dtype=np.int8)
    builders, start_positions = generate_builders(n_cols, n_rows)
    for index, pos in enumerate(start_positions):
        maze[pos] = index + 1

    while builders:
        builder_index = 0
        while builder_index < len(builders):
            b = builders[builder_index]
            if not b.remaining_distance:
                b.start_new_path()
            while b.is_hit_wall(n_cols, n_rows):
                b.start_new_path()
            b.move()
            if len(start_positions) > 1:
                if is_hit_other_path(maze, b):
                    builders.remove(b)
                    continue

            else:
                if maze[b.position] != 0:
                    builders.remove(b)
                    continue

            maze[b.position] = b.id
            builder_index += 1

    print_maze(maze)

    start_position = (random.randint(1, n_cols - 1), random.randint(1, n_rows - 1))
    while maze[start_position] == 0:
        start_position = (random.randint(1, n_cols - 1), random.randint(1, n_rows - 1))
        
    goal_position = (random.randint(1, n_cols - 1), random.randint(1, n_rows - 1))
    while maze[goal_position] == 0 or goal_position == start_position:
        goal_position = (random.randint(1, n_cols - 1), random.randint(1, n_rows - 1))

    print(goal_position)
    with open('tmp/goal_coordinates', 'w') as f:
        print(*goal_position, file=f)

    print(start_position)
    with open('tmp/start_coordinates', 'w') as f:
        print(*start_position, file=f)

if __name__ == '__main__':
        main()
