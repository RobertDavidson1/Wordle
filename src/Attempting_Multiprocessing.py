import multiprocessing
from data_initializer import ensure_data_exists
from helpers import load_words, load_colouring, heuristic
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


def compute_value(state, all_guesses, colouring_data, filtered_split_actions, shared_state, hash, depth=0, v_mem={}):
    if v_mem.get((depth, state)):return v_mem[(depth, state)]
    # Exit cases
    if depth == 6 or (depth == 5 and len(state) > 1): return (float("inf"), None)
    if depth == 5: return (1, None)
    if len(state) == 1: return (1, (state)[0])
    if len(state) == 2: return (1.5, (state)[0])

    if depth == 0: 
        current_list = filtered_split_actions
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
        if depth == 0:
            progress = int((index / len(current_list)) * 100)
            if progress % 20 == 0 and progress != last_printed_progress:
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

            value, _ = compute_value(next_state, all_guesses, colouring_data, [], shared_state, hash, depth + 1,)
            temp_score += next_states[next_state] * value

        if temp_score < state_value:
            state_value = temp_score
            best_word = action

        
    v_mem[(depth, state)] = (state_value, best_word)
    return state_value, best_word

def process_task(state, all_guesses, colouring_data, filtered_split_actions, shared_state, hash, result_queue):
    results = compute_value(state, all_guesses, colouring_data, filtered_split_actions, shared_state, hash)
    result_queue.put((multiprocessing.current_process().name, results))

def set_cpu_affinity(pid, core_id):
    try:
        os.sched_setaffinity(pid, {core_id})
        # print(f"Core : {core_id}")
    except AttributeError:
        print("CPU affinity setting is not supported on this platform.")
    except Exception as e:
        print(f"Error setting CPU affinity: {e}")

import time
if __name__ == "__main__":
    ensure_data_exists()

    PROCESSES = min(10, os.cpu_count())
    DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'data')
    GUESSES_PATH = os.path.join(DATA_DIRECTORY, 'allowed_guesses.txt')
    PRECOMPUTE_PATH = os.path.join(DATA_DIRECTORY, 'precompute.json')

    manager = multiprocessing.Manager()
    result_queue = manager.Queue()
    shared_state = manager.dict({'value': float("inf"), 'best_word': None})
    hash = manager.dict()

    colouring_data = load_colouring(PRECOMPUTE_PATH)
    all_guesses = load_words(GUESSES_PATH)
    state = ('scene', 'scone', 'scope', 'score', 'seedy', 'segue', 'seize', 'sense', 'serif', 'serum', 'serve', 'sheik', 'shine', 'shire', 'shone', 'shore', 'shove', 'siege', 'sieve', 'since', 'singe', 'smoke', 'snide', 'snipe', 'snore', 'speck', 'spend', 'sperm', 'spice', 'spike', 'spine', 'spire', 'spoke', 'spore', 'surge', 'swine', 'swore')

    filtered_split_actions = heuristic(all_guesses, state, colouring_data, PROCESSES)


    manager = multiprocessing.Manager()
    result_queue = manager.Queue()

  

    processes = [
        multiprocessing.Process(
            target=process_task,
            args=(state, all_guesses, colouring_data, filtered_split_actions[i], shared_state, hash, result_queue)
        ) for i in range(PROCESSES)
    ]

 
    start_time = time.time()
    i = 0
    for p in processes:
        i+=1
        p.start()
        set_cpu_affinity(p.pid, i)
        

    for p in processes:
        p.join()
    end_time = time.time()


    results = []
    print(f"\nRESULTS:")
    while not result_queue.empty():
        process_name, result = result_queue.get()
        results.append(result)
        print(f"{process_name:<10}: {result[1]} ({round(result[0],3)})")

    # Find the word with the smallest associated value
    min_value = float("inf")
    best_word = None
    for value, word in results:
        if value < min_value:
            min_value = value
            best_word = word

    print(f"All processes have finished execution. Best word: {best_word}, Value: {min_value}")
    print(f"Time taken: {end_time - start_time} seconds")
