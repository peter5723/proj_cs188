# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor. 
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    action_list = []
    start_state = problem.getStartState()
    explored_set = [start_state]
    frontier_stack = util.Stack()
    for item in problem.getSuccessors(start_state):
        frontier_stack.push((1, item)) #让frontier中的子节点知道自己是第k步走到/扩展到
    
    while not frontier_stack.isEmpty():
        cur_config = frontier_stack.pop()
        cur_step = cur_config[0]
        cur_state = cur_config[1][0] #item = successor state,action, stepCost
        cur_action = cur_config[1][1]
        if cur_state in explored_set:
            continue
        explored_set.append(cur_state)
        action_list.append(cur_action)
        if problem.isGoalState(cur_state):
            return action_list
        next_successors = problem.getSuccessors(cur_state)
        """
        for item in next_successors:
            if item[0] in explored_set:
                next_successors.remove(item)
        #终于让我找到这个bug了,python中非常有名的bug,在list中删除元素,一定要小心.
        #最好的办法是在副本中遍历.
        """
        for item in next_successors[:]:
            if item[0] in explored_set:
                next_successors.remove(item)
        if len(next_successors) == 0: #无解
            if (frontier_stack.isEmpty()):
                return []
            
            temp = frontier_stack.pop()
            next_step_num = temp[0]
            if next_step_num == 1:
                action_list = []
            else:
                action_list = action_list[0:next_step_num-1]
            frontier_stack.push(temp)
            #无解吧当前的action删除. 倒退到栈顶的步数
        else: #有解
            for item in next_successors:
                if item[0] not in explored_set:
                    frontier_stack.push((cur_config[0]+1, item))
    return action_list
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    action_list =  []
    frontier_queue = util.Queue()
    explored_set = []
    start_state = problem.getStartState()
    
    frontier_queue.push((start_state, []))
        
    while not frontier_queue.isEmpty():
        cur_config = frontier_queue.pop()
        cur_state = cur_config[0]
        cur_all_actions = cur_config[1]
        if problem.isGoalState(cur_state):
            return cur_all_actions
        if cur_state in explored_set:
            continue
        explored_set.append(cur_state)
        next_successors = problem.getSuccessors(cur_state)
        for child in next_successors[:]:
            if explored_set.count(child):
                next_successors.remove(child)
        if len(next_successors) == 0:
            continue
        for item in next_successors:
            child_all_actions = cur_all_actions[:]
            child_all_actions.append(item[1])
            frontier_queue.push((item[0], child_all_actions))
            
        #a list of triples, (successor state, action, stepCost)

       #TODO
    #    看了一下stackoverflow, 才发现有更简单的方法. 在数据结构中直接储存路径而不是节点.
    # 太聪明了.... 我tm花了4到5个小时写第一个dfs...wuyuzi
    return action_list
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    def priorityFunction(item):
        return item[1]
    #item是一个tuple, priorityFunction返回比较的依据也就是item[1]
    action_list =  []
    frontier_queue = util.PriorityQueueWithFunction(priorityFunction)
    explored_set = []
    start_state = problem.getStartState()
    
    frontier_queue.push((start_state, 0, [])) #state, cost, all actions

    min_all_cost = 0 
    now_all_cost = 0
    while not frontier_queue.isEmpty():
        cur_config = frontier_queue.pop()
        cur_state = cur_config[0]
        cur_cost = cur_config[1]
        cur_all_actions = cur_config[2]
        if problem.isGoalState(cur_state):
            return cur_all_actions
        #没毛病? 这种方法下(ucs)第一个弹出的理应是最优解
        if cur_state in explored_set:
            continue
        #一样的也有可能已经在之前就explore过了
        explored_set.append(cur_state)
        next_successors = problem.getSuccessors(cur_state)
        for item in next_successors[:]:
            if item[0] in explored_set:
                next_successors.remove(item)
        if len(next_successors)==0:
            continue
        for item in next_successors:
            item_actions = cur_all_actions[:]
            item_actions.append(item[1])
            item_all_cost = problem.getCostOfActions(item_actions)
            frontier_queue.push((item[0], item_all_cost, item_actions))
        
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    def priorityFunction(item):
        return item[1]
    action_list =  []
    frontier_queue = util.PriorityQueueWithFunction(priorityFunction)
    explored_set = []
    start_state = problem.getStartState()
    
    frontier_queue.push((start_state, 0, [])) #state, cost, all actions

    min_all_cost = 0 
    now_all_cost = 0
    while not frontier_queue.isEmpty():
        cur_config = frontier_queue.pop()
        cur_state = cur_config[0]
        cur_cost = cur_config[1]
        cur_all_actions = cur_config[2]
        if problem.isGoalState(cur_state):
            return cur_all_actions
        #没毛病? 这种方法下(ucs)第一个弹出的理应是最优解
        if cur_state in explored_set:
            continue
        #一样的也有可能已经在之前就explore过了
        explored_set.append(cur_state)
        next_successors = problem.getSuccessors(cur_state)
        for item in next_successors[:]:
            if item[0] in explored_set:
                next_successors.remove(item)
        if len(next_successors)==0:
            continue
        for item in next_successors:
            item_actions = cur_all_actions[:]
            item_actions.append(item[1])
            item_all_cost = problem.getCostOfActions(item_actions) + heuristic(item[0], problem)
            frontier_queue.push((item[0], item_all_cost, item_actions))
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
