# Project 1 - [Search in Pacman](https://www.cs.rpi.edu/~xial/Teaching/2019SAI/projects/search/search.html)

![maze](http://ai.berkeley.edu/projects/release/search/v1/001/maze.png#center)  
*All those colored walls,
Mazes give Pacman the blues,
So teach him to search.*

`search.py` - Where all of my search algorithms reside  
`searchAgents.py` -	Where all of my search-based agents reside.  
`pacman.py`	- The main file that runs Pacman games. This file describes a Pacman GameState type, which is used in this project.  
`game.py` - The logic behind how the Pacman world works. This file describes several supporting types like AgentState, Agent, Direction, and Grid.  
`util.py` - 	Useful data structures for implementing search algorithms.

* Question 1: Depth First Search (`search.py` - `depthFirstSearch`)
* Question 2: Breadth First Search (`search.py` - `breadthFirstSearch`)
* Question 3: Uniform Cost Search (`search.py` - `uniformCostSearch`)
* Question 4: A* Search (`search.py` - `aStarSearch`)
* Question 5: Corners Problem: Representation (`searchAgents.py` - `CornersProblem`)
* Question 6: Corners Problem: Heuristic (`searchAgents.py` - `cornersHeuristic`)
* Question 7: Eating All The Dots: Heuristic (`searchAgents.py` - `FoodSearchProblem`)
* Question 8: Suboptimal Search (`searchAgents.py` - `findPathToClosestDot`)
