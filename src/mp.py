import json
import concurrent.futures
import multiprocessing as mp

print(f"Loading actions")
guesses_file = "../data/allowed_guesses.txt"
with open(guesses_file, "r") as fhand:
    actions = [word.strip() for word in fhand]

print(f"Loading Colouring Data")
# Load the JSON data
with open("../data/precompute.json", "r") as file:
    colouring_data = json.load(file)
print(f"Completed")
   

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



def value_function(t, state, actions, v_mem, shared, lock, colouring_data):
    if (t, state) in v_mem:
        return v_mem[(t, state)]
    
    if t >= 6 or (t == 5 and len(state) > 1):
        return (float("inf"), None)
    if t == 5 or len(state) == 1:
        return (1, (state))
    elif len(state) == 2:
        return (1.5, (state)[0])

    state_value = float('inf')
    best_word = None
        
    for action in actions:
        if t == 1:
            print(f"Searching for best word: {actions.index(action) / len(actions): .3%}, Current word = {action}")
    
        transition_info = get_transition_info(state, action, colouring_data)
        temp = 1
        
        if len(transition_info.keys()) == 1 and tuple(transition_info.keys())[0] == state:
            continue
        
        temp += (2 * len(state) - 1) / len(state)

        for st1 in transition_info.keys():
            if temp >= state_value:
                break
            elif st1 == action:
                continue
            
            res, _ = value_function(t + 1, state=st1, actions=actions, v_mem=v_mem, shared=shared, lock=lock, colouring_data=colouring_data)
            temp += transition_info[st1] * res

        if temp < state_value:
            state_value = temp
            best_word = action

    # Update the shared state_value
    with lock:
        shared.state_value = min(shared.state_value, state_value)
    
    v_mem[(t, state)] = (state_value, best_word)
    return state_value, best_word


def value_function_wrapper(args):
    t, state, actions, v_mem, shared, lock, colouring_data = args
    return value_function(t, state, actions, v_mem, shared, lock, colouring_data)


import time
def main():
    
    state = ("stack", "staff", "staid", "stain", "stair", "stamp", "stand", "stank", "stark", "stash", "strap", "straw", "stray", "swath")
    
    # Get the number of available CPUs, with a max of 9
    max_cpu = 12
    cpu_count = min(max_cpu, mp.cpu_count())
    
    # Split the actions into cpu_count chunks
    num_chunks = cpu_count 
    chunk_size = len(actions) / num_chunks 
    indices = [int(i * chunk_size) for i in range(num_chunks + 1)] 
    chunks = [actions[indices[i]:indices[i + 1]] for i in range(len(indices) - 1)]
    
    chunks[0].insert(0,'prink')
    chunks[0] += state
    
    chunks = [tuple(chunk) for chunk in chunks]
    
    manager = mp.Manager()
    v_mem = manager.dict()
    shared = manager.Namespace()
    shared.state_value = float('inf')
    lock = manager.Lock()

    tasks = [(1, state, chunk, v_mem, shared, lock, colouring_data) for chunk in chunks]
    start_time = time.time()

    print(f"Loading {cpu_count} processes")
    with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count) as executor:
        results = list(executor.map(value_function_wrapper, tasks))

    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

    min_value, min_word = min(results, key=lambda x: x[0])
    print(f"\nBest word: {min_word}, ({min_value})")

if __name__ == "__main__":
    main()