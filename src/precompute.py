from collections import Counter
import os
import json
import platform

def clear_terminal():
    current_os = platform.system()
    if current_os == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def get_tile_coloring(guess, solution):
    result = ['-' for _ in range(len(guess))]  # Start with all white
    solution_counts = Counter(solution)

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


def load_words(file_path):
    with open(file_path, "r") as file_handle:
        word_array = [word.strip() for word in file_handle]
    return word_array


def create_precompute_json(DATA_DIRECTORY):
    GUESSES_PATH = os.path.join(DATA_DIRECTORY, 'allowed_guesses.txt')
    ANSWERS_PATH = os.path.join(DATA_DIRECTORY, 'allowed_answers.txt')
    PRECOMPUTE_PATH = os.path.join(DATA_DIRECTORY, 'precompute.json')

    guesses = load_words(GUESSES_PATH)
    answers = load_words(ANSWERS_PATH)

    colouring_hashmap = {}
    for i, word in enumerate(guesses):
        if i != 0 and i % (len(guesses) // 100) == 0:  # Clear terminal and show progress every 10%
            clear_terminal()
            print(f"Creating precompute.json | Progress: {i / len(guesses):.3%}")
        guess = [word]
        possible_colourings = {}
        
        for solution in answers:
            colouring = get_tile_coloring(guess, solution)
            possible_colourings[solution] = colouring

        colouring_hashmap[word] = possible_colourings
    
    with open(PRECOMPUTE_PATH, 'w') as json_file:
        json.dump(colouring_hashmap, json_file, indent=4)
        print("precompute.json created")