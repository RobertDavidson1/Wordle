from helpers import load_words, load_colouring, get_transition_info, clear_terminal, get_tile_colouring
from state_solver import next_best_guess
import json
import os

def load_data():
    DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'data')
    GUESSES_PATH = os.path.join(DATA_DIRECTORY, 'allowed_guesses.txt')
    ANSWERS_PATH = os.path.join(DATA_DIRECTORY, 'allowed_answers.txt')
    
    all_guesses = load_words(GUESSES_PATH)
    all_words = load_words(ANSWERS_PATH)
    colouring_data = load_colouring()

    return colouring_data, all_guesses, all_words

class GlobalParams:
    def __init__(self, colouring_data, all_guesses, all_words, processes):
        self.colouring_data = colouring_data
        self.all_guesses = all_guesses
        self.all_words = all_words
        self.processes = processes

def build_decision_tree(state, params, best_word, depth):
    # Initialize an empty dictionary to store the solved tree
    solved_tree = {}

    # Get the next states from the current state using the best word
    next_states = get_transition_info(state, best_word, params.colouring_data)
    next_states = list(next_states.keys())
    
    for next_state in next_states:
        # Calculate and print progress for shallow depthss
        if depth <= 2:
            progress = round(next_states.index(next_state) / len(next_states) * 100, 2)

            if depth == 1:
                clear_terminal()
                print(f"Overall Progress: {progress}% ")
            else: 
                print(f"Creating state tree: {progress}%")
        
        # Get the tile coloring for the best word and next state
        colouring = get_tile_colouring(best_word, next_state[0])
        
        # Determine the next best word using the next_best_guess function
        next_best_word = next_best_guess(params.processes, params.colouring_data, params.all_guesses, next_state, depth)

        # If the path is solved
        if colouring == "ggggg" and len(next_state) == 1:
            solved_tree["ggggg"] = next_state[0]
        
        else:
            # Recursively build the tree for the next states
            solved_tree[colouring] = {
                "best word": next_best_word,
                "next states": build_decision_tree(next_state, params, next_best_word, depth + 1)
            }
            
    return solved_tree

def build_and_save_tree():
    # Load necessary data
    colouring_data, all_guesses, all_words = load_data()

    # Determine the number of processes to use (up to 14 or the number of CPU cores)
    PROCESSES = min(10, os.cpu_count())

    # Initialize TreeBuilderParams with the loaded data and processes
    params = GlobalParams(colouring_data, all_guesses, all_words, PROCESSES)

    # Define the initial state and initialize depth to 0
    state = tuple(all_words)
    depth = 0
    
    print(f"Finding initial best word for initial state ({len(state)})")
    # Find the best starting word
    # best_word = next_best_guess(params.processes, params.colouring_data, params.all_guesses, state, depth)
    # print(f"Best Word = {best_word}")

    best_word = "salet"
    # Build the solved tree starting with the best word and initial state
    solved_tree = {
        "best word": best_word, 
        "next states": build_decision_tree(state, params, best_word, depth + 1)
    }

    # Define the path to save the solved game as JSON
    DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'data')
    SOLVED_JSON_PATH = os.path.join(DATA_DIRECTORY, 'decision_tree.json')
    
    # Export the solved tree to a JSON file
    with open(SOLVED_JSON_PATH, 'w') as f:
        json.dump(solved_tree, f, indent=4)

    print(f"Exported guesses to {SOLVED_JSON_PATH}.")


