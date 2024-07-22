import orjson
import os
import platform
import numpy as np

def clear_terminal():
    current_os = platform.system()
    if current_os == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def load_words(file_path):
    with open(file_path, "r") as file_handle:
        word_array = [word.strip() for word in file_handle]
    return word_array

def load_colouring():
    # Create the full path to the precompute.json file
    precompute_full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'precompute.json'))

    with open(precompute_full_path, "rb") as file:
        data = orjson.loads(file.read())
    return data

def get_transition_info(state, action, colouring_data):
    # Initialize an empty dictionary to store new states based on the action taken
    new_state = {}
    
    # Iterate through each possible solution in the current state
    for possible_solution in state:
        # Get the colouring for the current action and possible solution from the colouring_data
        colouring = colouring_data[action][possible_solution]
        
        # If the colouring is not already a key in new_state, add it with the current possible solution as its first value
        if colouring not in new_state:
            new_state[colouring] = [possible_solution]
        else:
            # If the colouring is already a key, append the current possible solution to the list of solutions
            new_state[colouring].append(possible_solution)
    
    # Create a dictionary to store the transition information
    # Keys are tuples of states, values are the the probability of transitioning into said state
    transition_info = {tuple(states): (len(states) / len(state)) for states in new_state.values()}
    
    # Return the transition information dictionary
    return transition_info

def get_tile_colouring(guess, solution):
    result = ['-'] * len(guess)  # Start with all white
    solution_counts = {}

    # Count occurrences of each character in the solution
    for char in solution:
        if char in solution_counts:
            solution_counts[char] += 1
        else:
            solution_counts[char] = 1

    # First pass: mark greens and reduce counts for correct letters
    for i in range(len(guess)):
        if guess[i] == solution[i]:
            result[i] = 'g'
            solution_counts[guess[i]] -= 1

    # Second pass: mark yellows, ensuring not to exceed the available count of each character
    for i in range(len(guess)):
        if result[i] == '-':  # Only check for yellow if it's not already green
            char = guess[i]
            if char in solution_counts and solution_counts[char] > 0:
                result[i] = 'y'
                solution_counts[char] -= 1

    # return the tile colouring
    return ''.join(result) 

def heuristic(actions, state,colouring_data, processes_to_split=1):
    percentile = 99.3
    transition_counts = {guess: len(get_transition_info(state, guess, colouring_data)) for guess in actions}
    lower_bound = np.percentile(list(transition_counts.values()), percentile)
    high_value_actions = [word for word, count in transition_counts.items() if count >= lower_bound]

    if processes_to_split != 1:
        split_arrays = np.array_split(high_value_actions, processes_to_split)
        return [list(map(str, sublist)) for sublist in split_arrays]
    else:
        return high_value_actions

def split_arrays(array, processes_to_split):
    if processes_to_split != 1:
        split_arrays = np.array_split(array, processes_to_split)
        return [list(map(str, sublist)) for sublist in split_arrays]
    else:
        return array