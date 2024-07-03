import multiprocessing
from data_initializer import ensure_data_exists
from helpers import load_words, load_colouring, heuristic_split_and_insert, heuristic
import os

color_codes = {
    0: '\033[91m',   # Red
    1: '\033[92m',   # Green
    2: '\033[93m',   # Yellow
    3: '\033[94m',   # Blue
    4: '\033[95m',   # Magenta
    5: '\033[96m',   # Cyan
    6: '\033[97m',   # White
    7: '\033[90m',   # Bright Black (Gray)
    8: '\033[31m',   # Dark Red
    9: '\033[32m',   # Dark Green
    10: '\033[33m',  # Dark Yellow
    11: '\033[34m',  # Dark Blue
    12: '\033[35m',  # Dark Magenta
    13: '\033[36m',  # Dark Cyan
    14: '\033[37m',  # Light Gray
    15: '\033[30m',  # Black
    'reset': '\033[0m'  # Reset
}

import re
def get_process_number():
    # Get the current process name
    process_name = multiprocessing.current_process().name
    
    # Use regular expression to extract the number
    match = re.search(r'Process-(\d+)', process_name)
    if match:
        print(int(match.group(1)))
        return int(match.group(1))
    return None

def color_string(string, color_number):
    color_code = color_codes.get(color_number, color_codes['reset'])
    return f"\033[0m{color_code}{string}{color_codes['reset']}"

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


def compute_value(state, all_guesses, colouring_data, proccessUnique_list, shared_state, depth=0, v_mem={}):
    if v_mem.get((depth, state)):return v_mem[(depth, state)]
    # Exit cases
    if depth == 6 or (depth == 5 and len(state) > 1): return (float("inf"), None)
    if depth == 5: return (1, None)
    if len(state) == 1: return (1, (state)[0])
    if len(state) == 2: return (1.5, (state)[0])

    if depth == 0: 
        current_list = proccessUnique_list
    else: 
        current_list = heuristic(all_guesses, state, colouring_data)

    state_value = float("inf")
    best_word = None
    last_printed_progress = -1

    for index, action in enumerate(current_list):
        if depth == 0:
            progress = int((index / len(current_list)) * 100)
            if progress % 10 == 0 and progress != last_printed_progress:
                process_name = get_process_number()
                string = f"{multiprocessing.current_process().name:<10} | Progress: {progress}%"
                print(color_string(string, process_name))
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

            value, _ = compute_value(next_state, all_guesses, colouring_data, [], shared_state, depth + 1,)
            temp_score += next_states[next_state] * value

        if temp_score < state_value:
            state_value = temp_score
            best_word = action

        
    v_mem[(depth, state)] = (state_value, best_word)
    return state_value, best_word

def process_task(state, all_guesses, colouring_data, processUnique_list, shared_state, result_queue):
    print(f"{multiprocessing.current_process().name} starting with {len(processUnique_list)} words")
    results = compute_value(state, all_guesses, colouring_data, processUnique_list, shared_state)
    result_queue.put((multiprocessing.current_process().name, results))

def set_cpu_affinity(pid, core_id):
    try:
        os.sched_setaffinity(pid, {core_id})
        print(f"Core : {core_id}|", end="")
    except AttributeError:
        print("CPU affinity setting is not supported on this platform.")
    except Exception as e:
        print(f"Error setting CPU affinity: {e}")

import numpy as np
if __name__ == "__main__":
    ensure_data_exists()

    PROCESSES = min(10, os.cpu_count())
    DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'data')
    GUESSES_PATH = os.path.join(DATA_DIRECTORY, 'allowed_guesses.txt')
    PRECOMPUTE_PATH = os.path.join(DATA_DIRECTORY, 'precompute.json')

    manager = multiprocessing.Manager()
    result_queue = manager.Queue()
    shared_state = manager.dict({'value': float("inf"), 'best_word': None})

    colouring_data = load_colouring(PRECOMPUTE_PATH)
    all_guesses = load_words(GUESSES_PATH)
    state = ('beech', 'beefy', 'begin', 'begun', 'being', 'bench', 'berry', 'binge', 'biome', 'booze', 'borne', 'bribe', 'bride', 'brine', 'broke', 'budge', 'check', 'chide', 'chime', 'choke', 'chore', 'coupe', 'credo', 'creme', 'crepe', 'crime', 'crone', 'crude', 'curve', 'debug', 'decor', 'decoy', 'decry', 'deign', 'demon', 'demur', 'denim', 'derby', 'deuce', 'diode', 'dirge', 'dodge', 'drive', 'drone', 'drove', 'dunce', 'ebony', 'edify', 'eerie', 'eking', 'endow', 'enemy', 'enjoy', 'ennui', 'envoy', 'epoch', 'epoxy', 'equip', 'erode', 'error', 'every', 'evoke', 'eying', 'feign', 'femme', 'femur', 'fence', 'ferry', 'fibre', 'fiend', 'fiery', 'force', 'forge', 'froze', 'fudge', 'fugue', 'gecko', 'geeky', 'genie', 'genre', 'gnome', 'gorge', 'gouge', 'grime', 'gripe', 'grope', 'grove', 'guide', 'hedge', 'hence', 'heron', 'hinge', 'horde', 'imbue', 'jerky', 'judge', 'juice', 'knife', 'medic', 'mercy', 'merge', 'merry', 'midge', 'mince', 'movie', 'needy', 'neigh', 'nerdy', 'nerve', 'niche', 'niece', 'nudge', 'ombre', 'opine', 'ounce', 'ovine', 'oxide', 'ozone', 'pence', 'penne', 'penny', 'perch', 'perky', 'phone', 'piece', 'pique', 'pixie', 'price', 'pride', 'prime', 'prize', 'probe', 'prone', 'prove', 'prude', 'prune', 'purge', 'query', 'queue', 'recur', 'reedy', 'reign', 'rerun', 'revue', 'rhyme', 'ridge', 'rogue', 'rouge', 'undue', 'urine', 'venom', 'venue', 'verge', 'verve', 'vogue', 'voice', 'wedge', 'weedy', 'weigh', 'weird', 'wench', 'where', 'whine', 'wince', 'wreck')
    processUnique_sublists = heuristic_split_and_insert(all_guesses, state, PROCESSES, colouring_data)

    manager = multiprocessing.Manager()
    result_queue = manager.Queue()

    extra_process = multiprocessing.Process(
        target=process_task,
        args=(state, all_guesses, colouring_data, list(state), shared_state, result_queue)
    )

    processes = [
        multiprocessing.Process(
            target=process_task,
            args=(state, all_guesses, colouring_data, processUnique_sublists[i], shared_state, result_queue)
        ) for i in range(PROCESSES)
    ]

    # extra_process.start()
    # set_cpu_affinity(extra_process.pid, 0)
    
    
    for i, p in enumerate(processes):
        p.start()
        set_cpu_affinity(p.pid, i + 1)

    # extra_process.join()
    for p in processes:
        p.join()


    results = []
    while not result_queue.empty():
        process_name, result = result_queue.get()
        results.append(result)
        print(f"Results from {process_name:<12}: {result}")


    # Find the word with the smallest associated value
    min_value = float("inf")
    best_word = None
    for value, word in results:
        if value < min_value:
            min_value = value
            best_word = word

    print(f"All processes have finished execution. Best word: {best_word}, Value: {min_value}")
