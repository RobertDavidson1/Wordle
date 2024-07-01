from data_initializer import ensure_data_exists
from helpers import load_words, load_colouring, clear_terminal
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

def compute_value(t, state, actions, v_mem, colouring_data):
    if v_mem.get((t, state)):
        return v_mem[(t, state)]
    if t == 6 or (t == 5 and len(state) > 1):
        return (float("inf"), None)
    elif t == 5:
        return (1, None)
    elif len(state) == 1:
        return (1, None)
    elif len(state) == 2:
        return (1.5, (state)[0])

    state_value = float("inf")
    best_word = None

    for action in actions:
       
        if t == 0:
            i = actions.index(action)
            if i!= 0 and i % (len(actions)//70) == 0:
                clear_terminal()
                print(f"Finding best word | Progress {actions.index(action) / len(actions)}")
        
        temp = 1
        next_states = get_transition_info(state, action, colouring_data)
        
        if len(next_states.keys()) == 1 and tuple(next_states.keys())[0] == state:
            continue

        temp += (2 * len(state) - 1) / len(state)

        for next_state in next_states.keys():
            if temp >= state_value:
                break
            elif "".join(next_state) == action:
                continue

            value, _ = compute_value(t+1, next_state, actions, v_mem, colouring_data)
            temp += next_states[next_state] * value

        if temp < state_value:
            state_value = temp
            best_word = action

    v_mem[(t, state)] = (state_value, best_word)
    return state_value, best_word



if __name__ == "__main__":
    ensure_data_exists()
    
    DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'data',)
    GUESSES_PATH = os.path.join(DATA_DIRECTORY, 'allowed_guesses.txt')
    PRECOMPUTE_PATH = os.path.join(DATA_DIRECTORY, 'precompute.json')


    state = ('shelf', 'shell', 'slice', 'slide', 'slime', 'slope', 'smell', 'smile', 'spell', 'swell')
    actions = tuple(load_words(GUESSES_PATH))
    colouring_data = load_colouring(PRECOMPUTE_PATH)
    
    state_value, best_word = compute_value(t=0, state=state, actions=actions,v_mem={}, colouring_data=colouring_data)
    print(best_word)