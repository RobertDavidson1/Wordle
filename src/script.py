import numpy as np

from collections import defaultdict
import json


guesses_file = "../data/allowed_guesses.txt"
with open(guesses_file, "r") as fhand:
    actions = [word.strip() for word in fhand]
   

with open(guesses_file, "r") as fhand:
    guesses = [word.strip() for word in fhand] 

answers_file = "../data/allowed_answers.txt"
with open(answers_file, "r") as fhand:
    answers = {word.strip() for word in fhand}


data_file = "../data/precompute.json"
# Open the JSON file
with open(data_file, 'r') as file:
    # Load the JSON data
    data = json.load(file)
    
def get_transition_info(state, action):
    new_state = {}
    for word in state:
        colouring = data[action][word] 
    
        if colouring not in new_state:
            new_state[colouring] = [word]
        else:
            new_state[colouring].append(word)
        
    transition_info = {frozenset(states): len(states) / len(state) for states in new_state.values()}

    return transition_info







from collections import defaultdict
from tqdm import tqdm

def value_function(t, state, actions, v_mem={}):

    if v_mem is None:
        v_mem = defaultdict(lambda: (np.inf, None))

    v_mem_key = (t, frozenset(state))  # frozenset is used to ensure hashability of the state
    if v_mem_key in v_mem:
         return v_mem[v_mem_key]
    
    if t >= 6 or (t == 5 and len(state) != 1):
        return (np.inf, None)
    if t == 5 or len(state) == 1:
        return (1, list(state))
    if len(state) == 2:
        return (1.5, list(state)[0])
    if len(state) == 0:
        return (np.inf, None)
    
    
    state_value = np.inf
    best_action = None

    
    for action in actions:
        
        
        next_states = get_transition_info(state, action)
        if frozenset({action}) in next_states.keys():
            del next_states[frozenset({action})]
        
        if len(next_states) == 1 and next(iter(next_states.keys())) == state:
            continue
    
        temp = 1    
        for st1, p in next_states.items():
            min_possible_value = (2 * len(st1) - 1) / len(st1)
            if temp + min_possible_value * p >= state_value:
                break
            
        
        for st1, p in next_states.items():
            if st1 == frozenset({action}):
                continue
            
            value, _ = value_function(t+1, st1, actions)
            temp += p*value
            if temp >= state_value:  

                break
            
        if temp < state_value and temp != np.inf: 
            state_value = temp
            best_action = action
            
           

           
    v_mem[(t, state)] = (state_value, best_action)
    return state_value, best_action



def process_actions(t, state, actions):
    # Assuming value_function and other necessary functions are defined
    return value_function(t, state, actions)

def main():
    state = frozenset({'baste', 'caste', 'haste', 'paste', 'taste', 'waste'})

    max_cpu = 2
    cpu_count = min(max_cpu, mp.cpu_count())
    chunk_size = len(actions) // cpu_count 
    



    action_chunks = [actions[i:i + chunk_size] for i in range(0, len(actions), chunk_size)]
    print(len(action_chunks[0]), len(action_chunks[1]))
    print(action_chunks[0][0], action_chunks[1][0])
    
    
    with mp.Pool(cpu_count) as pool:
            t = 1
            results = pool.starmap(process_actions, [(t, state, chunk) for chunk in action_chunks])
    
    
    min_value, min_word = min(results, key=lambda x: x[0])
    print("Minimum value:", min_value)
    print("Corresponding word:", min_word)  
    print("\n",results)

    
import time
if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    execution_time_mins = execution_time // 60
    execution_time_seconds = execution_time % 60
    print(f"Execution time: {execution_time}")
    print(f"{execution_time_mins}mins {execution_time_seconds}s")
    
