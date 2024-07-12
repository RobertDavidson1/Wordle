import multiprocessing
from helpers import heuristic, clear_terminal
import os

def get_transition_info(state, action, colouring_data):
    new_state = {}
    for word in state:
        colouring = colouring_data[action][word]
        if colouring not in new_state:
            new_state[colouring] = [word]
        else:
            new_state[colouring].append(word)
    transition_info = {tuple(states): (len(states) / len(state)) for states in new_state.values()}
    return transition_info

def compute_value(state, all_guesses, colouring_data, initial_action_split, hash, depth, v_mem={}):
    
    if v_mem.get((depth, state)): return v_mem[(depth, state)]
    if depth == 6 or (depth == 5 and len(state) > 1): return (1, state[0])
    if depth == 5: return (1, state[0])
    if len(state) == 1: return (1, (state)[0])


    
    if depth == 0: 
        current_list = initial_action_split
    else: 
        if state not in hash.keys():
            current_list = heuristic(all_guesses, state, colouring_data)
            hash[state] = current_list
        else:
            current_list = hash[state]

    state_value = float("inf")
    best_word = None
    last_printed_progress = -1

    for index, action in enumerate(current_list):
        if depth == 1:
            progress = int((index / len(current_list)) * 100)
            if progress != last_printed_progress:
                print(f"{multiprocessing.current_process().name:<10} | Progress: {progress}%")
                last_printed_progress = progress

        temp_score = 1
        next_states = get_transition_info(state, action, colouring_data)
        
        if len(next_states.keys()) == 1 and tuple(next_states.keys())[0] == state:
            continue

        temp_score += (2 * len(state) - 1) / len(state)

        if temp_score >= state_value:
            break

        for next_state in next_states.keys():
            if "".join(next_state) == action:
                continue
    
            value, _ = compute_value(next_state, all_guesses, colouring_data, [], hash, depth + 1,v_mem)
            temp_score += next_states[next_state] * value

        if temp_score < state_value:
            state_value = temp_score
            best_word = action

        
    v_mem[(depth, state)] = (state_value, best_word)
    return state_value, best_word

def process_task(state, all_guesses, colouring_data, filtered_split_actions, hash, result_queue, depth):
    
    results = compute_value(state, all_guesses, colouring_data, filtered_split_actions, hash, depth)
    result_queue.put((multiprocessing.current_process().name, results))

def solve_state(PROCESSES, colouring_data, all_guesses, state, optimal_action_subsets, depth):
    manager = multiprocessing.Manager()
    result_queue = manager.Queue()
    hash = manager.dict()

    processes = [multiprocessing.Process(
                target=process_task,
                args=(state, all_guesses, colouring_data, 
                      optimal_action_subsets[i], hash, result_queue, depth)
                ) for i in range(PROCESSES)
                ]
 
    for i, p in enumerate(processes):
        p.start()
        os.sched_setaffinity(p.pid, {i+1})

    for p in processes:
        p.join()

    results = [result_queue.get() for _ in range(result_queue.qsize())]
    best_word = min(results, key=lambda x: x[1][0])[1][1]

    return best_word

def Solver(PROCESSES, colouring_data, all_guesses, state, depth):
    if len(state) == 1 or len(state) == 2:
        return state[0]
    else:
        optimal_action_subsets = heuristic(all_guesses, state, colouring_data, PROCESSES)
        print(f"Length of state : {len(state):<4} | First 3 words = {state[:3]}")
        best_word = solve_state(PROCESSES, colouring_data, all_guesses, state, optimal_action_subsets, depth)
    return best_word

