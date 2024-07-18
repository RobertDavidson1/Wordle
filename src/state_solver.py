from helpers import heuristic, get_transition_info
import multiprocessing
import os

# Class to encapsulate global parameters
class GlobalParams:
    def __init__(self, all_guesses, colouring_data, state_cache, processes):
        self.all_guesses = all_guesses
        self.colouring_data = colouring_data
        self.state_cache = state_cache
        self.processes = processes

# Function to compute the value of a given state
def compute_value(state, params, initial_action_split, depth, v_mem={}):
    # Check if the value of this state at this depth is already computed and cached
    if v_mem.get((depth, state)): 
        return v_mem[(depth, state)]
    
    # Base cases for recursion termination
    if depth == 6 or (depth == 5 and len(state) > 1): 
        return (1, state[0])
    if depth == 5: 
        return (1, state[0])
    if len(state) == 1: 
        return (1, state[0])

    # Determine the current list of actions to consider
    if depth == 0: 
        # the initial_action_split for depth == 0 will result in the same list
        # we precompute this split instead of redundantly for each process
        current_list = initial_action_split
    else: 
        # After depth == 0, the optimal list will begin to differ
        # Store this in state_cache
        if state not in params.state_cache.keys():
            current_list = heuristic(params.all_guesses, state, params.colouring_data)
            params.state_cache[state] = current_list
        else:
            current_list = params.state_cache[state]

    state_value = float("inf")  # Initialize state value to infinity
    best_word = None  # Initialize best word to None
    last_printed_progress = -1  # Initialize last printed progress for status updates

    # Iterate through each action in the current list
    for index, action in enumerate(current_list):
        if depth == 1:
            progress = int((index / len(current_list)) * 100)
            if progress != last_printed_progress:
                print(f"{multiprocessing.current_process().name:<10} | Progress: {progress}%")
                last_printed_progress = progress

        temp_score = 1  # Initialize temporary score
        next_states = get_transition_info(state, action, params.colouring_data)  # Get possible next states
        
        if depth == 0:
            next_states = dict(sorted(next_states.items(), key=lambda item: item[1], reverse=True))


        if len(next_states.keys()) == 1 and tuple(next_states.keys())[0] == state:
            continue

        temp_score += (2 * len(state) - 1) / len(state)

        if temp_score >= state_value:
            break

        # Compute value for each possible next state
        for next_state in next_states.keys():
            if depth == 0:
                print(len(next_state))
                
            
            if "".join(next_state) == action:
                continue
    
            value, _ = compute_value(next_state, params, [], depth + 1, v_mem)
            temp_score += next_states[next_state] * value

        if temp_score < state_value:
            state_value = temp_score
            best_word = action

    # Cache the computed value for this state and depth
    v_mem[(depth, state)] = (state_value, best_word)
    return state_value, best_word

# Function to process a task in a separate process
def process_task(state, params, filtered_split_actions, result_queue, depth):
    results = compute_value(state, params, filtered_split_actions, depth)
    result_queue.put((multiprocessing.current_process().name, results))

# Function to solve the state using multiple processes
def solve_state(params, state, optimal_action_subsets, depth):
    manager = multiprocessing.Manager()
    result_queue = manager.Queue()

    # Create and start multiple processes
    processes = [multiprocessing.Process(
                target=process_task,
                args=(state, params, optimal_action_subsets[i], result_queue, depth)
                ) for i in range(params.processes)
                ]
 
    for i, p in enumerate(processes):
        p.start()
        os.sched_setaffinity(p.pid, {i+1})  # Assign process to a specific CPU core

    # Wait for all processes to complete
    for p in processes:
        p.join()

    # Collect results from the result queue
    results = [result_queue.get() for _ in range(result_queue.qsize())]
    best_word = min(results, key=lambda x: x[1][0])[1][1]

    return best_word

from helpers import split_arrays
# Main next_best_guess function that decides the best word for a given state
def next_best_guess(PROCESSES, colouring_data, all_guesses, state, depth):
    if len(state) == 1 or len(state) == 2:
        return state[0]
    else:
        if depth == 0:
            print(f"Length of state : {len(state):<4}")
            array = ['tarse', "crane", "slate", "salet", "trace"]
            optimal_action_subsets = split_arrays(array, PROCESSES)
        else:
            optimal_action_subsets = heuristic(all_guesses, state, colouring_data, PROCESSES)

        PROCESSES = len(optimal_action_subsets)
    
        # Initialize GlobalParams
        state_cache = {}
        params = GlobalParams(all_guesses, colouring_data, state_cache, PROCESSES)

        best_word = solve_state(params, state, optimal_action_subsets, depth)
        return best_word