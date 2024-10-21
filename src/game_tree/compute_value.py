# game_tree/compute_value.py

import numpy as np
from .tree_node import TreeNode
from .helpers import getTransitionInfo
from .heuristics import getHeuristic
from .params import GlobalParams

import numpy as np
from collections import defaultdict



def computeValue(state, depth, params : GlobalParams, v_mem=None):
    """
    Optimized computeValue function with enhanced memoization and minimized overhead.
    """

    if v_mem is None:
        v_mem = {}
    
    # Use tuple for state_key if state is immutable
    state_key = tuple(state)
    key = (depth, state_key)
    
    if key in v_mem:
        return v_mem[key]
    
    state_len = len(state)
    if depth >= 5 or state_len == 1:
        return (1, state[0])
    
    # Retrieve or compute currentList
    if state_key not in params.stateCache:
        currentList = getHeuristic(params.allActions, params.colouringArray, state)
        params.stateCache[state_key] = currentList
    else:
        currentList = params.stateCache[state_key]
    
    stateValue = float("inf")
    bestWord = None
    score_increment = (2 * state_len - 1) / state_len
    initialTempScore = 1 + score_increment
    for action in currentList:

        tempScore = initialTempScore
        nextStates = getTransitionInfo(state, action, params.colouringArray, state_len)
        
        num_next = len(nextStates)
        if num_next == 0:
            continue
        elif num_next == 1:
            next_state = next(iter(nextStates))
            if next_state == state_key:
                continue
        
        if tempScore >= stateValue:
            break  # Prune this branch
        
        for nextState, prob in nextStates.items():
            if nextState[0] == action:
                continue  # Skip invalid transitions

            # Recursively compute the value of the next state
            value, _ = computeValue(nextState, depth + 1, params, v_mem)
            tempScore += prob * value
        
        if tempScore < stateValue:
            stateValue = tempScore
            bestWord = action
    
    # Memoize the result
    v_mem[key] = (stateValue, bestWord)
    return (stateValue, bestWord)

