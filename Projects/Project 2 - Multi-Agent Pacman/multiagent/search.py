# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:"""

    # print "Start:", problem.getStartState()
    # print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    # print "Start's successors:", problem.getSuccessors(problem.getStartState())
    #"""
    "*** YOUR CODE HERE ***"
    #A search state in this problem is a tuple (pacmanPosition, foodGrid)
    fringe = util.Stack()
    visited = []
    start = problem.getStartState()
    fringe.push((start, [])) #{(s, null)}
    while not fringe.isEmpty():
    	search_state = fringe.pop()
    	state, path = search_state[0], search_state[1]
    	if problem.isGoalState(state): return path #success
    	elif state in visited: continue #skip
    	else:
    		#expand v(search_state), insert resulting nodes into fringe
    		visited.append(state)
    		L = problem.getSuccessors(state)
    		expand(L, problem, path, fringe)
    return "Failure"

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    fringe = util.Queue()
    visited = []
    start = problem.getStartState()
    fringe.push((start, [])) #{(s, null)}
    while not fringe.isEmpty():
    	search_state = fringe.pop()
    	state, path = search_state[0], search_state[1]
    	if problem.isGoalState(state): return path #success
    	elif state in visited: continue #skip
    	else:
    		#expand v(search_state), insert resulting nodes into fringe
    		visited.append(state)
    		L = problem.getSuccessors(state)
    		expand(L, problem, path, fringe)
    return "Failure"

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue() #Cost based priority
    visited = []
    start = problem.getStartState()
    fringe.push((start, []), 0) #{(s, null), 0 (start node = 0 *cumulative* cost)}
    while not fringe.isEmpty():
    	search_state = fringe.pop()
    	state, path = search_state[0], search_state[1]
    	if problem.isGoalState(state): return path #success
    	elif state in visited: continue #skip
    	else:
    		#expand v(search_state), insert resulting nodes into fringe
    		visited.append(state)
    		L = problem.getSuccessors(state)
    		expand(L, problem, path, fringe, True)
    return "Failure"

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue() #Cost based priority
    visited = []
    start = problem.getStartState()
    fringe.push((start, []), heuristic(start, problem)) #{(s, null), 0 + heuristic)}
    while not fringe.isEmpty():
    	search_state = fringe.pop()
    	state, path = search_state[0], search_state[1]
    	if problem.isGoalState(state): return path #success
    	elif state in visited: continue #skip
    	else:
    		#expand v(search_state), insert resulting nodes into fringe with f(v)=g(v)+h(v)
    		visited.append(state)
    		L = problem.getSuccessors(state)
    		expand(L, problem, path, fringe, True, heuristic)
    return "Failure"


def expand(nbrs, problem, path, fringe, cost = False, heuristic = nullHeuristic):
    if cost:
        #For graph algorithms in which there is an associated cost/heuristic(UCS, A*)
        for nbr in nbrs:
            nbr_state, nbr_path = nbr[0], nbr[1]
            new_path = path + [nbr_path]
            total_cost = problem.getCostOfActions(new_path) + heuristic(nbr_state, problem)
            fringe.push((nbr_state, new_path), total_cost)
    else:
        #For graph algorithms in which all weights in the graph are equal(DFS, BFS)
        for nbr in nbrs:
            nbr_state, nbr_path = nbr[0], nbr[1]
            new_path = path + [nbr_path]
            fringe.push((nbr_state, new_path))

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
