# Artificial-Intelligence
This repository contains 2 programs that are courseworks assigned by module “Artificial Intelligence” at King's College London. These programs are developed in Python 2.

##	Coursework 1 <br>
*	In this coursework, breadth-first search (BFS) and 2D list (grid) are used to design an agent that automatically moves to minimize its distance between foods or to maximize its distance between ghosts.
Inspired by the instruction of practical exercises, my partial agent is a combination of hungry agent, corner seeking agent and survival agent. The fundamental strategy is that when there are no ghosts nearby, pacman just moves to the direction that minimize its distance between foods, and in order to make sure pacman can collect all of the foods in the map, the (x, y) coordinates of foods in four corners are automatically added to the food list. On the other hand, when the ghosts are nearby, pacman has to stop looking for foods, and to escape to the direction that maximize its distance between ghosts.
![image](https://github.com/dean03055045/Artificial-Intelligence/blob/master/pic%20for%20readme/workflow1.png)


##	Coursework 2 <br>
* In this coursework, Markov Decision Process (MDP) is applied to design an agent that moves in a non-deterministic way in a fully observational world. And with the help of 2D grids of maps, Maximum Expected Utility (MEU) is used for decision-making.
Inspired by the instruction of practical exercises, a 2D grid class is built to produce a map for storing the utility of each coordinates. The main strategy of MDP agent is to assign positive reward to foods, negative reward to ghosts, slightly negative reward to blank space (to urge pacman to move). After setting these rewards, with the application of Bellman equation and value iteration, final utility map is conducted and used with MEU to make the final move. It is worth noting that, for safety, reward of the neighbor cells of ghosts are also set to be negative. Furthermore, to speed up the game, the time of ghosts remaining scared is also taken into account (but set it to a safety value), when ghosts are scared, pacman should ignore them and eat foods as fast as it can.
![image](https://github.com/dean03055045/Artificial-Intelligence/blob/master/pic%20for%20readme/workflow2.png)


