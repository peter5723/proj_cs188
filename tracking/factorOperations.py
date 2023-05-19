# factorOperations.py
# -------------------
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

from typing import List
from bayesNet import Factor
import functools
from util import raiseNotDefined


def joinFactorsByVariableWithCallTracking(callTrackingList=None):

    def joinFactorsByVariable(factors: List[Factor], joinVariable: str):
        """
        Input factors is a list of factors.
        Input joinVariable is the variable to join on.

        This function performs a check that the variable that is being joined on 
        appears as an unconditioned variable in only one of the input factors.

        Then, it calls your joinFactors on all of the factors in factors that 
        contain that variable.

        Returns a tuple of 
        (factors not joined, resulting factor from joinFactors)
        """

        if not (callTrackingList is None):
            callTrackingList.append(('join', joinVariable))

        currentFactorsToJoin = [
            factor for factor in factors
            if joinVariable in factor.variablesSet()
        ]
        currentFactorsNotToJoin = [
            factor for factor in factors
            if joinVariable not in factor.variablesSet()
        ]

        # typecheck portion
        numVariableOnLeft = len([
            factor for factor in currentFactorsToJoin
            if joinVariable in factor.unconditionedVariables()
        ])
        if numVariableOnLeft > 1:
            print("Factor failed joinFactorsByVariable typecheck: ", factor)
            raise ValueError(
                "The joinBy variable can only appear in one factor as an \nunconditioned variable. \n"
                + "joinVariable: " + str(joinVariable) + "\n" + ", ".join(
                    map(str, [
                        factor.unconditionedVariables()
                        for factor in currentFactorsToJoin
                    ])))

        joinedFactor = joinFactors(currentFactorsToJoin)
        return currentFactorsNotToJoin, joinedFactor

    return joinFactorsByVariable


joinFactorsByVariable = joinFactorsByVariableWithCallTracking()

########### ########### ###########
########### QUESTION 2  ###########
########### ########### ###########


def joinFactors(factors: List[Factor]):
    """
    Input factors is a list of factors.  
    
    You should calculate the set of unconditioned variables and conditioned 
    variables for the join of those factors.

    Return a new factor that has those variables and whose probability entries 
    are product of the corresponding rows of the input factors.

    You may assume that the variableDomainsDict for all the input 
    factors are the same, since they come from the same BayesNet.

    joinFactors will only allow unconditionedVariables to appear in 
    one input factor (so their join is well defined).

    Hint: Factor methods that take an assignmentDict as input 
    (such as getProbability and setProbability) can handle 
    assignmentDicts that assign more variables than are in that factor.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    setsOfUnconditioned = [
        set(factor.unconditionedVariables()) for factor in factors
    ]
    if len(factors) > 1:
        intersect = functools.reduce(lambda x, y: x & y, setsOfUnconditioned)
        if len(intersect) > 0:
            print("Factor failed joinFactors typecheck: ", factor)
            raise ValueError(
                "unconditionedVariables can only appear in one factor. \n" +
                "unconditionedVariables: " + str(intersect) +
                "\nappear in more than one input factor.\n" +
                "Input factors: \n" + "\n".join(map(str, factors)))
    "*** YOUR CODE HERE ***"

    # 下面两个是helper func
    def getNewVari(old_uncon, old_con, uncon, con):
        #一定要这样的(我是说copy)
        new_con = old_con.copy()
        new_uncon = old_uncon.copy()
        if old_uncon == [] and old_con == []:
            return (uncon, con)
        for i in uncon:
            if i not in new_uncon:
                new_uncon.add(i)
            if i in new_con:
                new_con.remove(i)
        for j in con:
            if j not in new_con and j not in new_uncon:
                new_con.add(j)
        return new_uncon, new_con

    def canMul(old_vari, new_vari):
        # 只有在：新的变量与旧的变量同时出现时取值相同
        # 或者：新的变量根本就不出现在旧的变量中的时候
        # 可以执行概率的相乘
        for key in new_vari.keys():
            if key in old_vari.keys():
                if (old_vari[key] != new_vari[key]):
                    return False
        return True

    old_uncon = set()
    old_con = set()
    #old_factor
    tmp_factor = Factor(old_uncon, old_con, {})
    for factor in factors:
        uncon = factor.unconditionedVariables()
        con = factor.conditionedVariables()
        new_vari_dict = factor.variableDomainsDict()
        #更新后的new_uncon,new_con
        new_uncon, new_con = getNewVari(old_uncon, old_con, uncon, con)
        new_factor = Factor(new_uncon, new_con, new_vari_dict)
        if len(old_uncon) == 0:
            tmp_factor = factor
            old_con = con
            old_uncon = uncon
            continue
        #tmp_factor = Factor(old_con, con, new_vari_dict) or new_factor
        #更新概率
        for vari_t in tmp_factor.getAllPossibleAssignmentDicts():
            prob_t = tmp_factor.getProbability(vari_t)
            for vari_n in factor.getAllPossibleAssignmentDicts():
                prob_n = factor.getProbability(vari_n)
                # 对里面的每一个变量，
                # 只有在：新的变量与旧的变量同时出现时取值相同
                # 或者：新的变量根本就不出现在旧的变量中的时候
                # 可以执行概率的相乘
                if canMul(vari_t, vari_n):
                    new_prob = prob_n * prob_t
                    new_ass_dict = {**vari_t, **vari_n}
                    new_factor.setProbability(new_ass_dict, new_prob)
        tmp_factor = new_factor
        old_con = new_con
        old_uncon = new_uncon
    return new_factor
    "*** END YOUR CODE HERE ***"


########### ########### ###########
########### QUESTION 3  ###########
########### ########### ###########


def eliminateWithCallTracking(callTrackingList=None):

    def eliminate(factor: Factor, eliminationVariable: str):
        """
        Input factor is a single factor.
        Input eliminationVariable is the variable to eliminate from factor.
        eliminationVariable must be an unconditioned variable in factor.
        
        You should calculate the set of unconditioned variables and conditioned 
        variables for the factor obtained by eliminating the variable
        eliminationVariable.

        Return a new factor where all of the rows mentioning
        eliminationVariable are summed with rows that match
        assignments on the other variables.

        Useful functions:
        Factor.getAllPossibleAssignmentDicts
        Factor.getProbability
        Factor.setProbability
        Factor.unconditionedVariables
        Factor.conditionedVariables
        Factor.variableDomainsDict
        """
        # autograder tracking -- don't remove
        if not (callTrackingList is None):
            callTrackingList.append(('eliminate', eliminationVariable))

        # typecheck portion
        if eliminationVariable not in factor.unconditionedVariables():
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Elimination variable is not an unconditioned variable " \
                            + "in this factor\n" +
                            "eliminationVariable: " + str(eliminationVariable) + \
                            "\nunconditionedVariables:" + str(factor.unconditionedVariables()))

        if len(factor.unconditionedVariables()) == 1:
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Factor has only one unconditioned variable, so you " \
                    + "can't eliminate \nthat variable.\n" + \
                    "eliminationVariable:" + str(eliminationVariable) + "\n" +\
                    "unconditionedVariables: " + str(factor.unconditionedVariables()))
        "*** YOUR CODE HERE ***"
        con = factor.conditionedVariables()
        uncon = factor.unconditionedVariables()
        varidict = factor.variableDomainsDict()
        uncon.remove(eliminationVariable)
        all_value_of_eliVal = varidict[eliminationVariable]  #这个变量的所有取值
        new_factor = Factor(uncon, con, varidict)
        for vari_n in new_factor.getAllPossibleAssignmentDicts():
            prob = 0
            for vari_o in factor.getAllPossibleAssignmentDicts():
                vari_o_copy = vari_o.copy()
                vari_o_copy.pop(eliminationVariable)
                if vari_o_copy == vari_n:  #(判断是否是子集)(笨笨的)
                    prob += factor.getProbability(vari_o) #是的话就加
            new_factor.setProbability(vari_n, prob)
        return new_factor
        "*** END YOUR CODE HERE ***"

    return eliminate


eliminate = eliminateWithCallTracking()
