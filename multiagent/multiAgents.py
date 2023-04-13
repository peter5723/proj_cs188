# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
from pacman import GameState


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [
            self.evaluationFunction(gameState, action) for action in legalMoves
        ]
        bestScore = max(scores)
        bestIndices = [
            index for index in range(len(scores)) if scores[index] == bestScore
        ]
        chosenIndex = random.choice(
            bestIndices)  # Pick randomly among the best
        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates
        ]
        "*** YOUR CODE HERE ***"

        nowFoodList = currentGameState.getFood().asList()

        ghostsPos = [ghostState.getPosition() for ghostState in newGhostStates]
        foodList = newFood.asList()
        score = 0

        minFoodDist = 99999
        minFoodGhostDist = 99999
        nextfood = None
        for food in foodList:
            foodDist = manhattanDistance(food, newPos)
            if foodDist < minFoodDist:
                minFoodDist = foodDist
                nextfood = food
        if len(nowFoodList) > len(foodList):  #下一步吃到了食物
            score += 1000
        else:
            score += 500 / minFoodDist
        # food 很麻烦，到新的状态以后，就直接把食物吃掉了，得到的foodlist不包含想吃掉的那个
        #哈哈哈哈我好聪明看上面几行已经解决了
        minGhostDist = 999999
        for ghostPos in ghostsPos:
            dist = manhattanDistance(ghostPos, newPos)
            #   distFood = manhattanDistance(ghostPos, nextfood)
            if dist < minGhostDist:
                minGhostDist = dist
        #   if distFood < minFoodGhostDist:
        #       minFoodGhostDist = distFood
        if minGhostDist <= 2:
            score -= 1000
        elif newPos in ghostsPos:
            score -= 2000
        else:
            score += 1000

        #if minFoodGhostDist <= 1:
        #      score -= 200

        # if newPos in foodList:
        #    # score += 1000
        ## else:
        #    score += 1000/minFoodDist
        #
        #如果没有最优解导致随机的话不太好
        #我草，没有想到，还有stop这种，要是太差还不如stop
        return score


def scoreEvaluationFunction(currentGameState: GameState):
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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #注意，题给的深度不是树的深度，而是回合数的意思。
        #当然 回合数*agent数 就是我们所需要的深度了
        agentIndex = self.index  #这个agent的index,0 is pacman, !0 is ghost

        def getScoreAndAction(gameState: GameState, agentIndex, depth,
                              dstDepth):
            numAgents = gameState.getNumAgents()
            #输入当前的状态和当前的深度和目标的深度,当前的
            #返回这个节点的分数和达到这个分数所采取的下一步动作，递归。(是tree中的分不是实际的分，不要混淆)
            if gameState.isWin() or gameState.isLose():
                #递归出口1，游戏结束。
                return self.evaluationFunction(gameState), None
            if depth == dstDepth:
                #递归出口2，已经达到了所需要探险的深度
                return self.evaluationFunction(gameState), None
            actionsList = gameState.getLegalActions(agentIndex)
            #如何判断gameState返回的动作是属于哪一个agent的呢?sb, 有参数的
            stateList = []
            for action in actionsList:
                stateList.append(
                    gameState.generateSuccessor(agentIndex, action))

            miniMaxScore, _ = getScoreAndAction(stateList[0],
                                                (agentIndex + 1) % numAgents,
                                                depth + 1, dstDepth)
            action = actionsList[0]
            for i, state in enumerate(stateList[1:]):
                actionsList_1 = actionsList[1:]
                score, _ = getScoreAndAction(state,
                                             (agentIndex + 1) % numAgents,
                                             depth + 1, dstDepth)
                if agentIndex == 0:
                    if score > miniMaxScore:
                        miniMaxScore = score
                        action = actionsList_1[i]
                else:
                    if score < miniMaxScore:
                        miniMaxScore = score
                        action = actionsList_1[i]

            return miniMaxScore, action

        dstDepth = self.depth * gameState.getNumAgents()
        score, action = getScoreAndAction(gameState, agentIndex, 0, dstDepth)
        #好好好，从第0层开始，行了吧
        return action

        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # 原来我完完全全就理解错了，怎么写出对的代码呢？
        agentIndex = self.index

        def getScoreAndAction(gameState: GameState, agentIndex, depth,
                              dstDepth):
            if agentIndex == 0:
                return maxScoreAndAction(gameState, agentIndex, depth,
                                         dstDepth, -999999, 999999)
            else:
                return minScoreAndAction(gameState, agentIndex, depth,
                                         dstDepth, -999999, 999999)

        def maxScoreAndAction(gameState: GameState, agentIndex, depth,
                              dstDepth, a, b):
            numAgents = gameState.getNumAgents()
            if gameState.isWin() or gameState.isLose() or depth == dstDepth:
                return self.evaluationFunction(gameState), None
            #叶子结点
            actionsList = gameState.getLegalActions(agentIndex)
            #下面对普通节点操作。
            miniMaxScore = -999999
            best_action = None
            for action in actionsList:
                state = gameState.generateSuccessor(agentIndex, action)
                score, _ = minScoreAndAction(state,
                                             (agentIndex + 1) % numAgents,
                                             depth + 1, dstDepth, a, b)
                if score > miniMaxScore:
                    miniMaxScore = score
                    best_action = action
                    if miniMaxScore > b:
                        return miniMaxScore, best_action
                a = max(a, miniMaxScore)
            return miniMaxScore, best_action

        def minScoreAndAction(gameState: GameState, agentIndex, depth,
                              dstDepth, a, b):
            numAgents = gameState.getNumAgents()
            if gameState.isWin() or gameState.isLose() or depth == dstDepth:
                return self.evaluationFunction(gameState), None
            #叶子结点
            actionsList = gameState.getLegalActions(agentIndex)
            #下面对普通节点操作。
            miniMaxScore = 999999
            #无穷的意思表示一开始是随意的、无限制的状态，可以理解不？
            best_action = None
            for action in actionsList:
                state = gameState.generateSuccessor(agentIndex, action)
                if (agentIndex + 1) % numAgents == 0:
                    score, _ = maxScoreAndAction(state,
                                                 (agentIndex + 1) % numAgents,
                                                 depth + 1, dstDepth, a, b)
                else:
                    score, _ = minScoreAndAction(state,
                                                 (agentIndex + 1) % numAgents,
                                                 depth + 1, dstDepth, a, b)
                if score < miniMaxScore:
                    miniMaxScore = score
                    best_action = action
                    #想了想，就算是上面有好几个miniAgent也是直接与a比较就行了
                    if miniMaxScore < a:
                        #ma de被坑了明明说取等的时候要剪枝的，结果测试又不减了。
                        return miniMaxScore, best_action

                b = min(b, miniMaxScore)
            return miniMaxScore, best_action

        dstDepth = self.depth * gameState.getNumAgents()
        _, action = getScoreAndAction(gameState, agentIndex, 0, dstDepth)
        return action
        util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
