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
    print(f"{filtered_split_actions[:3]}")
    results = compute_value(state, all_guesses, colouring_data, filtered_split_actions, shared_state, hash)
    result_queue.put((multiprocessing.current_process().name, results))

def set_cpu_affinity(pid, core_id):
    try:
        os.sched_setaffinity(pid, {core_id})
    except AttributeError:
        print("CPU affinity setting is not supported on this platform.")
    except Exception as e:
        print(f"Error setting CPU affinity: {e}")

import time
if __name__ == "__main__":
    ensure_data_exists()

    PROCESSES = min(14, os.cpu_count())
    DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'data')
    GUESSES_PATH = os.path.join(DATA_DIRECTORY, 'allowed_guesses.txt')
    PRECOMPUTE_PATH = os.path.join(DATA_DIRECTORY, 'precompute.json')
    ANSWERS_PATH = os.path.join(DATA_DIRECTORY, 'allowed_answers.txt')


    manager = multiprocessing.Manager()
    result_queue = manager.Queue()
    shared_state = manager.dict({'value': float("inf"), 'best_word': None})
    hash = manager.dict()

    colouring_data = load_colouring(PRECOMPUTE_PATH)
    all_guesses = load_words(GUESSES_PATH)
    all_answers = load_words(ANSWERS_PATH)
    state = ('biddy', 'bingo', 'birch', 'bobby', 'bongo', 'booby', 'boozy', 'bough', 'bound', 'brick', 'bring', 'brink', 'briny', 'brood', 'brook', 'broom', 'brown', 'buddy', 'buggy', 'bunch', 'bunny', 'buxom', 'chick', 'chirp', 'chock', 'choir', 'chord', 'chuck', 'chump', 'chunk', 'churn', 'cinch', 'civic', 'comfy', 'comic', 'conch', 'condo', 'conic', 'corny', 'couch', 'cough', 'crick', 'crimp', 'crock', 'crony', 'crook', 'croup', 'crowd', 'crown', 'crumb', 'crump', 'cubic', 'cumin', 'curio', 'curry', 'curvy', 'cynic', 'dingo', 'dingy', 'dizzy', 'dodgy', 'doing', 'donor', 'dough', 'dowdy', 'downy', 'dowry', 'drink', 'droop', 'drown', 'druid', 'drunk', 'duchy', 'dummy', 'dumpy', 'dying', 'finch', 'fizzy', 'fjord', 'foggy', 'forgo', 'forum', 'found', 'frock', 'frond', 'frown', 'fungi', 'funky', 'funny', 'furor', 'furry', 'fuzzy', 'giddy', 'going', 'goody', 'goofy', 'gourd', 'grimy', 'grind', 'groin', 'groom', 'group', 'grown', 'gruff', 'gumbo', 'gummy', 'guppy', 'hippo', 'hippy', 'hobby', 'honor', 'horny', 'hound', 'howdy', 'humid', 'humor', 'humph', 'hunch', 'hunky', 'hurry', 'hydro', 'icing', 'idiom', 'inbox', 'incur', 'ionic', 'irony', 'ivory', 'jiffy', 'juicy', 'jumbo', 'jumpy', 'juror', 'kinky', 'knock', 'known', 'micro', 'mimic', 'minim', 'minor', 'moody', 'moron', 'morph', 'mound', 'mourn', 'mucky', 'muddy', 'mummy', 'munch', 'murky', 'myrrh', 'ninny', 'nymph', 'occur', 'onion', 'opium', 'ovoid', 'owing', 'phony', 'picky', 'piggy', 'pinch', 'pinky', 'pooch', 'poppy', 'porch', 'pouch', 'pound', 'prick', 'primo', 'prior', 'privy', 'prong', 'proof', 'proud', 'proxy', 'pubic', 'pudgy', 'puffy', 'punch', 'puppy', 'pygmy', 'quick', 'quirk', 'rhino', 'rigid', 'rigor', 'robin', 'rocky', 'roomy', 'rough', 'round', 'rowdy', 'ruddy', 'rugby', 'rumor', 'undid', 'unify', 'union', 'unzip', 'vigor', 'vivid', 'vouch', 'vying', 'which', 'whiff', 'whiny', 'whoop', 'widow', 'wimpy', 'winch', 'windy', 'woody', 'woozy', 'wordy', 'worry', 'wound', 'wring', 'wrong', 'wrung', 'young')

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
    for i, p in enumerate(processes):
        p.start()
        set_cpu_affinity(p.pid, i + 1) 
        

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
