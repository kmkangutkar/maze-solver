# graphics
USE_GUI = False
USE_RENDER = True
BLOCK_SIZE = 40 # pixels

# maze
START = (0, 0)
GOAL = (0, 15)
MAZE_CHOICES = ['tmp/example_maze', 'example_maze2', 'tmp/example_maze_not_working']
MAZE_FILE = MAZE_CHOICES[0]
ACTION_SPACE = ['up', 'down', 'left', 'right']

# learning
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.8
E_GREEDY = 0.99
MOVEMENT_REWARD = -0.04
GOAL_REWARD = 1
PIT_REWARD = -100
