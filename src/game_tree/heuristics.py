from numba import njit, prange
import numpy as np

@njit(parallel=True, fastmath=True, cache=True)
def compute_unique_counts_bitmask(coloringArray, state, actions):
    """
    Computes the number of unique colors for each action using bitmasking.
    
    Parameters:
    - coloringArray: 2D NumPy array of shape (num_actions, num_states) with dtype=np.uint8
    - state: 1D NumPy array of state indices with dtype=np.uint16
    - actions: 1D NumPy array of actions with dtype=np.uint16
    
    Returns:
    - unique_counts: 1D NumPy array with the count of unique colors for each action
    """
    num_actions = actions.shape[0]
    unique_counts = np.empty(num_actions, dtype=np.int64)
    
    for i in prange(num_actions):
        action = actions[i]
        seen0 = 0x0  # Colors 0-63
        seen1 = 0x0  # Colors 64-127
        seen2 = 0x0  # Colors 128-191
        seen3 = 0x0  # Colors 192-255
        unique = 0
        
        for j in range(state.shape[0]):
            s = state[j]
            color = coloringArray[action, s]
            
            if color < 64:
                bit = 1 << color
                if (seen0 & bit) == 0:
                    seen0 |= bit
                    unique += 1
            elif color < 128:
                c = color - 64
                bit = 1 << c
                if (seen1 & bit) == 0:
                    seen1 |= bit
                    unique += 1
            elif color < 192:
                c = color - 128
                bit = 1 << c
                if (seen2 & bit) == 0:
                    seen2 |= bit
                    unique += 1
            else:
                c = color - 192
                bit = 1 << c
                if (seen3 & bit) == 0:
                    seen3 |= bit
                    unique += 1
        
        unique_counts[i] = unique
    
    return unique_counts

@njit(cache=True)
def compute_percentile_numba(arr, percentile):
    """
    Computes the desired percentile using a partial sort (similar to np.percentile).
    
    Parameters:
    - arr: 1D NumPy array of numerical values (dtype=np.int64)
    - percentile: Float representing the desired percentile (0-100)
    
    Returns:
    - threshold: The value at the specified percentile
    """
    n = arr.size
    if n == 0:
        raise ValueError("Cannot compute percentile of empty array.")
    if not 0 <= percentile <= 100:
        raise ValueError("Percentile must be between 0 and 100.")
    
    # Calculate the index for the desired percentile
    k = int(np.ceil((percentile / 100.0) * n)) - 1
    k = max(k, 0)  # Ensure k is not negative
    k = min(k, n - 1)  # Ensure k does not exceed array bounds
    
    # Correctly use np.partition with a positive index
    threshold = np.partition(arr, k)[k]
    
    return threshold


@njit(cache=True)
def filter_and_sort_numba(actions, counts, percentile):
    """
    Filters actions based on the percentile threshold and sorts them in descending order.
    
    Parameters:
    - actions: 1D NumPy array of actions (dtype=np.uint16)
    - counts: 1D NumPy array of unique counts (dtype=np.int64)
    - percentile: Float representing the desired percentile (0-100)
    
    Returns:
    - sorted_filtered_actions: 1D NumPy array of filtered and sorted actions
    """
    # Compute the threshold
    threshold = compute_percentile_numba(counts, percentile)
    
    # Determine the number of actions meeting the threshold
    mask = counts >= threshold
    filtered_size = 0
    for i in range(mask.size):
        if mask[i]:
            filtered_size += 1
    
    # Initialize arrays to hold filtered actions and counts
    filtered_actions = np.empty(filtered_size, dtype=np.uint16)
    filtered_counts = np.empty(filtered_size, dtype=np.int64)
    
    idx = 0
    for i in range(actions.size):
        if mask[i]:
            filtered_actions[idx] = actions[i]
            filtered_counts[idx] = counts[i]
            idx += 1
    
    # Sort the filtered counts in descending order and reorder actions accordingly
    sorted_indices = np.argsort(-filtered_counts)
    sorted_filtered_actions = np.empty(filtered_size, dtype=np.uint16)
    for i in range(filtered_size):
        sorted_filtered_actions[i] = filtered_actions[sorted_indices[i]]
    
    return sorted_filtered_actions

def getHeuristic(actions, colouringArray, state):
    """
    Retrieves high-value actions sorted by their unique coloring counts in descending order.
    
    Parameters:
    - actions: Iterable of possible actions (e.g., list or NumPy array) with dtype=np.uint16
    - colouringArray: 2D NumPy array representing coloring information with dtype=np.uint8
    - state: 1D NumPy array of state indices with dtype=np.uint16
    
    Returns:
    - highValueActions: List of actions sorted by their counts in descending order
    """
    percentile = 99.3
    
    # Ensure inputs are contiguous and correctly typed
    actions_np = np.ascontiguousarray(np.array(actions, dtype=np.uint16))
    state_np = np.ascontiguousarray(np.array(state, dtype=np.uint16))
    
    # Compute unique counts using Numba-optimized function
    unique_counts = compute_unique_counts_bitmask(colouringArray, state_np, actions_np)
    
    # Filter and sort using Numba-optimized function
    highValueActions_np = filter_and_sort_numba(actions_np, unique_counts, percentile)
    
    return highValueActions_np.tolist()
