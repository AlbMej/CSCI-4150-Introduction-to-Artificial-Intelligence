# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        closestFoodDist = 2**32
        curFoodNum, newFood = currentGameState.getFood().count(), newFood.asList()
        score = 0
        # This new position does not result in food being eaten
        if len(newFood) == curFoodNum: 
            # Find closest food to new position
            closestFoodDist = min( min(closestFoodDist, manhattanDistance(food, newPos)) for food in newFood)      
        else:
            closestFoodDist = 0
        # Closest food now holds the highest score 
        score = -closestFoodDist
        # Score will decrease as distance near Ghost decreases
        for ghost in newGhostStates:  
            ghostDist = manhattanDistance(ghost.getPosition(), newPos)
            score -= 2**(2 - ghostDist)
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def value(self, state, agentIndex, curDepth):	
        pacman = 0
        terminalState = [state.isLose(), state.isWin(), curDepth >=  self.depth*self.numAgents] #curDepth >=  self.depth*self.numAgents
        if any(terminalState): return self.evaluationFunction(state)
        if self.index == self.numAgents-1: agentIndex = 0
        if agentIndex == pacman: return self.maxValue(state, pacman, curDepth)[0]
        else: return self.minValue(state, agentIndex, curDepth)[0]

    def minValue(self, state, ghostIndex, curDepth):
        minAction = float('inf'), Directions.STOP
        actions = state.getLegalActions(ghostIndex)
        for action in actions:
            successor = state.generateSuccessor(ghostIndex, action)
            newDepth = curDepth + 1
            nextAgent = newDepth % self.numAgents #To wrap around indices
            newAction = (self.value(successor, nextAgent, newDepth), action)
            minAction = min(minAction, newAction)
        return minAction

    def maxValue(self, state, pacmanIndex, curDepth):
        maxAction = float('-inf'), Directions.STOP
        actions = state.getLegalActions(0)
        for action in actions:
            successor = state.generateSuccessor(pacmanIndex, action)
            newDepth = curDepth + 1
            nextAgent = newDepth % self.numAgents #To wrap around indices
            newAction = (self.value(successor, nextAgent, newDepth), action)
            maxAction = max(maxAction, newAction)
        return maxAction

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        #Get best outcome for Pacman. 
        #Outcome: (value, action) -> (9, West)
        self.numAgents = gameState.getNumAgents() 
        minimaxAction = self.maxValue(gameState,0,0)[1]
        return minimaxAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def value(self, state, agentIndex, curDepth, alpha, beta):	
        pacman = 0
        terminalState = [state.isLose(), state.isWin(), curDepth >=  self.depth*self.numAgents] #curDepth >=  self.depth*self.numAgents
        if any(terminalState): return self.evaluationFunction(state)
        if self.index == self.numAgents-1: agentIndex = 0
        if agentIndex == pacman: return self.maxValue(state, pacman, curDepth, alpha, beta)[0]
        else: return self.minValue(state, agentIndex, curDepth, alpha, beta)[0]

    def minValue(self, state, ghostIndex, curDepth, alpha, beta):
        v = float('inf'), Directions.STOP
        actions = state.getLegalActions(ghostIndex)
        for action in actions:
            successor = state.generateSuccessor(ghostIndex, action)
            newDepth = curDepth + 1
            nextAgent = newDepth % self.numAgents #To wrap around indices
            newAction = (self.value(successor, nextAgent, newDepth, alpha, beta), action)
            v = min(v, newAction)
            if v[0] < alpha: return v 
            beta = min(beta, v[0])
        return v

    def maxValue(self, state, pacmanIndex, curDepth, alpha, beta):
        v = float('-inf'), Directions.STOP
        actions = state.getLegalActions(0)
        for action in actions:
            successor = state.generateSuccessor(pacmanIndex, action)
            newDepth = curDepth + 1
            nextAgent = newDepth % self.numAgents #To wrap around indices
            newAction = (self.value(successor, nextAgent, newDepth, alpha, beta), action)
            v = max(v, newAction)
            if v[0] > beta: return v 
            alpha = max(alpha, v[0])
        return v

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = float("-inf")
        beta  = float("inf")
        self.numAgents = gameState.getNumAgents() 
        alphaBetaAction = self.maxValue(gameState,0,0, alpha, beta)[1]
        return alphaBetaAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def value(self, state, agentIndex, curDepth):	
        pacman = 0
        terminalState = [state.isLose(), state.isWin(), curDepth >=  self.depth*self.numAgents] #curDepth >=  self.depth*self.numAgents
        if any(terminalState): return self.evaluationFunction(state)
        if self.index == self.numAgents-1: agentIndex = 0
        if agentIndex == pacman: return self.maxValue(state, pacman, curDepth)[0]
        else: return self.expValue(state, agentIndex, curDepth)

    def expValue(self, state, ghostIndex, curDepth):
        values = [] 
        actions = state.getLegalActions(ghostIndex) #successors
        for action in actions: 
            successor = state.generateSuccessor(ghostIndex, action)
            newDepth = curDepth + 1
            nextAgent = newDepth % self.numAgents #To wrap around indices
            newAction = self.value(successor, nextAgent, newDepth)
            values.append(newAction)
        expectation = sum(values)/(len(values))
        return expectation

    def maxValue(self, state, pacmanIndex, curDepth):
        v = float('-inf'), Directions.STOP
        actions = state.getLegalActions(0)
        for action in actions:
            successor = state.generateSuccessor(pacmanIndex, action)
            newDepth = curDepth + 1
            nextAgent = newDepth % self.numAgents #To wrap around indices
            newAction = (self.value(successor, nextAgent, newDepth), action)
            v = max(v, newAction)
        return v

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        self.numAgents = gameState.getNumAgents() 
        expectimaxAction = self.maxValue(gameState,0,0)[1]
        return expectimaxAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      The total score is subtracted by the sum of all the distances to all the food pellets. This is to keep Pacman 
      close to all food as the less food there is, the less there is subtracted from the total score. I then keep a score 
      for the ghost cpu and subtract that from the total score. The closer the ghost, the higher his score is. His score increases
      at an exponential rate. However, I also subtract from the ghost score when the ghost is in a scared state. His score is lowered
      at an exponential rate. I also add bonus points to the total score when the ghost is scared. The exponentially decreasing ghost 
      score and addition of bonus points is to give Pacman an incentive to go towards the ghost when he is in a scared state. 
    """
    "*** YOUR CODE HERE ***"
    pacmanPos = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates() 
    ScaredTimesPos = [(ghostState.scaredTimer, ghostState.getPosition()) for ghostState in ghostStates]
    curFood = currentGameState.getFood().asList()

    totalFoodDist = 0
    for foodPos in curFood:
        totalFoodDist += manhattanDistance(foodPos, pacmanPos)

    # Ghost score increases the closer the ghost is to pacman
    ghostScore = 0 
    scaredGhostBonus = 0
    for (scaredTimer, ghostPos) in ScaredTimesPos:  
    	ghostDist = float('inf')
        if scaredTimer == 0:
    	    ghostDist = manhattanDistance(ghostPos, pacmanPos)
            ghostScore += 2**(4 - ghostDist)
        else:
        	#Bonus points for ghost being in a scared state
        	ghostScore -= 2**(2 - ghostDist)
        	scaredGhostBonus += 2**(scaredTimer)

    return (currentGameState.getScore() - totalFoodDist) - ghostScore + scaredGhostBonus

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()