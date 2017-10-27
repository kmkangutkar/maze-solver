# graphics
USE_GUI = True
USE_RENDER = True
BLOCK_SIZE = 40 # pixels

# maze
START = (0, 0)
GOAL = (19, 0)
MAZE_FILE = 'example_maze2' # 'tmp/example_maze'

# learning
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.8
E_GREEDY = 0.99
MOVEMENT_REWARD = -0.04
GOAL_REWARD = 1
PIT_REWARD = -100
