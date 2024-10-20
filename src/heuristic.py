import numpy as np
import json
from tqdm import tqdm
from helperFunctions import *
import numpy as np
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

def init_pool(colouringArray, wordIndices, state_indices_array):
    global global_colouringArray
    global global_wordIndices
    global global_state_indices_array
    global_colouringArray = colouringArray
    global_wordIndices = wordIndices
    global_state_indices_array = state_indices_array

def count_unique_colorings(action):

    actionIndex = global_wordIndices.get(action)
    if actionIndex is None:
        # If the action word is not found, return 0 unique colorings
        return (action, 0)
    
    # Retrieve all coloring codes for this action against the state
    colorings = global_colouringArray[actionIndex, global_state_indices_array]
    
    # Count the number of unique colorings using NumPy's vectorized operations
    unique_count = np.unique(colorings).size
    
    return (action, unique_count)

def totalUniqueColourings(words: list[str], colouringArray: np.ndarray, wordIndices: dict, processes_to_split: int = cpu_count()) -> dict:

    # Precompute state indices as a NumPy array for efficiency
    state_indices = [wordIndices[word] for word in words if word in wordIndices]
    state_indices_array = np.array(state_indices, dtype=int)

    # Initialize the multiprocessing Pool with the initializer
    with Pool(processes=processes_to_split, initializer=init_pool, initargs=(colouringArray, wordIndices, state_indices_array)) as pool:
        # Use tqdm to display a progress bar
        results = list(tqdm(pool.imap_unordered(count_unique_colorings, words), total=len(words), desc="Counting Unique Colorings"))

    # Convert the list of tuples into a dictionary
    transitionCounts = dict(results)

    return transitionCounts

def getHeuristic(words, colouringArray, wordIndices):

    percentile = 99.3
    transitionCounts = totalUniqueColourings(words, colouringArray, wordIndices, 10)
    lowerBound =  np.percentile(list(transitionCounts.values()), percentile)
    high_value_action = [action for action, count in transitionCounts.items() if count >= lowerBound]
    return high_value_action