from collections import Counter
import os
import json
from helpers import clear_terminal, load_words

def get_tile_coloring(guess, solution):
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

    return ''.join(result)

def create_precompute_json(DATA_DIRECTORY):
    GUESSES_PATH = os.path.join(DATA_DIRECTORY, 'allowed_guesses.txt')
    ANSWERS_PATH = os.path.join(DATA_DIRECTORY, 'allowed_answers.txt')
    PRECOMPUTE_PATH = os.path.join(DATA_DIRECTORY, 'precompute.json')

    guesses = load_words(GUESSES_PATH)
    answers = load_words(ANSWERS_PATH)

    colouring_hashmap = {}
    for i, guess in enumerate(guesses):
        if i != 0 and i % (len(guesses) // 70) == 0:  # Clear terminal and show progress every 10%
            clear_terminal()
            print(f"Creating precompute.json | Progress: {i / len(guesses):.3%}")


        possible_colourings = {}
        for solution in answers:
            colouring = get_tile_coloring(guess, solution)
            possible_colourings[solution] = colouring

        colouring_hashmap[guess] = possible_colourings
    
    with open(PRECOMPUTE_PATH, 'w') as json_file:
        json.dump(colouring_hashmap, json_file, indent=4)
        print("precompute.json created ✅")