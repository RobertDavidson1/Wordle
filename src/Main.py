from data_initializer import ensure_data_exists
from helpers import load_words, load_colouring, get_transition_info, get_tile_coloring, clear_terminal
from Solver import Solver
import os
import json

def load_data(PROCESSES):
    DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'data')
    GUESSES_PATH = os.path.join(DATA_DIRECTORY, 'allowed_guesses.txt')
    PRECOMPUTE_PATH = os.path.join(DATA_DIRECTORY, 'precompute.json')
    ANSWERS_PATH = os.path.join(DATA_DIRECTORY, 'allowed_answers.txt')
    colouring_data = load_colouring(PRECOMPUTE_PATH)
    all_guesses = load_words(GUESSES_PATH)
    all_words = load_words(ANSWERS_PATH)

    return colouring_data, all_guesses, all_words

def tree(state, colouring_data, all_guesses, all_words, PROCESSES, best_word, depth):
    solved_tree = {}
    next_states = get_transition_info(state, best_word, colouring_data)
    next_states = list(dict(sorted(next_states.items(), key=lambda item: len(item[0]), reverse=True)).keys())
    

    for next_state in next_states:
        if depth <= 2:
            progress = round(next_states.index(next_state) / len(next_states)*100, 2)
                
            if depth == 1:
                clear_terminal()
                print(f"Overall Progress: {progress}% ")
            elif len(next_state) >= 30: # reduncant to print otherwise - too fast
                print(f"Creating state tree: {progress}%")
        colouring = get_tile_coloring(best_word, next_state[0])
        next_best_word = Solver(PROCESSES, colouring_data, all_guesses, next_state, depth)  
        
        if colouring == "ggggg" and len(next_state) == 1:
            solved_tree["ggggg"] = next_state[0]
        else:
            solved_tree[colouring] = {
                "best word": next_best_word,
                "next states": tree(next_state, colouring_data, all_guesses, all_words, PROCESSES, next_best_word, depth + 1)
            }

    return solved_tree

def main():
    ensure_data_exists()
    PROCESSES = min(14, os.cpu_count())
    colouring_data, all_guesses, all_words = load_data(PROCESSES)

    state = tuple(all_words)
    best_word = "slate"
    
    solved_tree = {
        "best word": best_word, 
        "next states": tree(state, colouring_data, all_guesses, all_words, PROCESSES, best_word=best_word, depth = 1)
    }


    DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'data')
    SOLVED_JSON_PATH = os.path.join(DATA_DIRECTORY, 'solved_game.json')
    # Export guesses as JSON
    with open(SOLVED_JSON_PATH, 'w') as f:
        
        
        json.dump(solved_tree, f, indent=4)

    print(f"Exported guesses to {SOLVED_JSON_PATH}.")

if __name__ == "__main__":
    main()
