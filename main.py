"""
Red rectangle:          explorer.
Black rectangles:       pits        [reward = -1].
Yellow bin circle:      goal        [reward = +1].
All other states:       ground      [reward = 0].
"""

from maze_env import Maze
from rl_brain import QLearningTable

def main():
    # take constants as input
    n_iterations = 100   

    # create the maze (create canvas and accept goal state)
    maze = Maze()
    rl = QLearningTable(actions=list(range(maze.n_actions)))
    
    print('G:', maze.canvas.coords(maze.goal))

    maze.after(100, update, maze, rl, n_iterations)
    maze.mainloop()

    # accept start state and show traversal from start to goal

def update(maze, rl, n_iterations):
    for iteration in range(n_iterations):
        # initial observation
        observation = maze.reset()

        done = False
        step_count = 0
        while not done:
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
        #print (rl.q_table)
        if reward == 1:
            print(iteration, '\tsteps:\t', step_count)
    # end of game
    print('game over')
    maze.destroy()

if __name__ == "__main__":
        main()
