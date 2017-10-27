"""
Red rectangle:          explorer.
Black rectangles:       pits        [reward = -1].
Yellow bin circle:      goal        [reward = +1].
All other states:       ground      [reward = 0].
"""

USE_GUI = False
USE_RENDER = False

from maze_env import Maze, MazeWithoutGui
from rl_brain import QLearningTable
import time

def main():
    # take constants as input
    n_iterations = 1000 

    # create the maze (create canvas and accept goal state)
    if USE_GUI:
        maze = Maze()
    else:
        maze = MazeWithoutGui()

    rl = QLearningTable(actions=list(range(maze.n_actions)))

    if USE_GUI:
        maze.after(100, update, maze, rl, n_iterations)
        maze.mainloop()
    else:
        time.sleep(0.1)
        update(maze, rl, n_iterations)
    
def update(maze, rl, n_iterations):
    successful_iterations = []
    for iteration in range(n_iterations):
        # initial observation
        observation = maze.reset()

        done = False
        step_count = 0
        while not done:
            if USE_GUI and USE_RENDER:
                # fresh maze
                maze.render()
            # rl choose action based on observation
            action = rl.choose_action(str(observation))

            # rl take action and get next observation and reward
            observation_new, reward, done = maze.step(action)

            # rl learn from this transition
            rl.learn(str(observation), action, reward, str(observation_new))

            # swap observation
            observation = observation_new
            step_count += 1
            #print('\r', step_count, observation, end='')
#       if reward == 1:
 #           print(iteration, '\tsteps:\t', step_count)
       
        if reward == 1:
            result = '#'
            successful_iterations.append((iteration, step_count)) 
        else:
            result = ''
#        print(iteration, step_count, result, sep='\t')
        print('\r', iteration, len(successful_iterations), end='')
    # end of game
    #print('game over')
    print('SI', successful_iterations, sep='\n')
    with open('tmp/successes', 'w') as f:
        for s in successful_iterations:
            print(*s, file=f)
    print(min([x[1] for x in successful_iterations]))
    

    if USE_GUI:
        maze.destroy()
        with open('gui', 'w') as f:
            print(rl.q_table, file=f)
    else:
        with open('no_gui', 'w') as f:
            print(rl.q_table, file=f)


if __name__ == "__main__":
        main()
