from tqdm import tqdm
import numpy as np

from numba import njit, prange
from joblib import Parallel, delayed, cpu_count
from multiprocessing import Pool, cpu_count

# USING NUMBA
@njit(parallel=True)
def compute_unique_counts(coloringArray, state, actions):
    unique_counts = np.empty(len(actions), dtype=np.int64)
    for i in prange(len(actions)):
        action = actions[i]
        colorings = coloringArray[action, state]
        unique = 0
        seen = {}
        for color in colorings:
            if color not in seen:
                seen[color] = True
                unique += 1
        unique_counts[i] = unique
    return unique_counts

def totalUniqueColourings(actions, coloringArray, state) -> dict:
    # Convert actions to a NumPy array for better performance with numba
    actions_np = np.array(actions)
    
    # Compute unique counts using numba for parallel execution
    unique_counts = compute_unique_counts(coloringArray, state, actions_np)
    
    # Create a dictionary mapping actions to their unique counts
    transitionCounts = dict(zip(actions_np, unique_counts))
    
    return transitionCounts

def getHeuristic(actions, colouringArray, state):
    percentile = 99.3
    transitionCounts = totalUniqueColourings(actions, colouringArray, state)
    counts = np.array(list(transitionCounts.values()))
    lowerBound = np.percentile(counts, percentile)
    highValueActions = [action for action, count in transitionCounts.items() if count >= lowerBound]
    return highValueActions



# USING JOB LIB
# def uniqueColourings(action, coloringArray, state):
#     colorings = coloringArray[action, state]
#     unique_count = np.unique(colorings).size
#     return (action, unique_count)



# def totalUniqueColourings(actions, coloringArray, state) -> dict:
#     results = Parallel(n_jobs=cpu_count(), backend='loky')(
#         delayed(uniqueColourings)(action, coloringArray, state) for action in actions)
#     transitionCounts = dict(results)
#     return transitionCounts


## USING MULTIPROCESSING
# def init_pool(colouringArray, state):
#     global global_colouringArray
#     global global_State

#     global_colouringArray = colouringArray
#     global_State = state

# def uniqueColourings(action):
#     colorings = global_colouringArray[action, global_State]
#     unique_count = np.unique(colorings).size
#     return (action, unique_count)

# def totalUniqueColourings(actions, coloringArray, state) -> dict:
    
#     processes = max(cpu_count(), 10)
    
#     with Pool(processes=processes, initializer=init_pool, initargs=(coloringArray, state)) as pool:
#         results = list(tqdm(pool.imap_unordered(uniqueColourings, actions), total=len(actions), desc="Counting Unique Colorings"))

#     transitionCounts = dict(results)

#     return transitionCounts


