# graphics
USE_GUI = False
USE_RENDER = True
BLOCK_SIZE = 20 # pixels

PIT_CHAR = 'P'
OPEN_CHAR = '.'
START_CHAR = 'S'
GOAL_CHAR = 'G'

# maze
START = (0, 0)
GOAL = (4, 5)
MAZE_CHOICES = ['tmp/example_maze', 'example_maze2', 'tmp/example_maze_not_working', 'tmp/sample_maze']
MAZE_FILE = MAZE_CHOICES[3]
ACTION_SPACE = ['up', 'down', 'left', 'right']

# learning
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.8
E_GREEDY = 0.99
MOVEMENT_REWARD = -1 #-0.04
GOAL_REWARD = 1
PIT_REWARD = -100
N_ITERATIONS = 1000
