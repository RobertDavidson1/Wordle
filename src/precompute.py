import os
import json
from helpers import clear_terminal, load_words, get_tile_colouring

# Function to create precompute.json file with all possible colorings
def create_precompute_json(DATA_DIRECTORY):
    # Define paths for guesses, answers, and the output precompute JSON file
    GUESSES_PATH = os.path.join(DATA_DIRECTORY, 'allowed_guesses.txt')
    ANSWERS_PATH = os.path.join(DATA_DIRECTORY, 'allowed_answers.txt')
    PRECOMPUTE_PATH = os.path.join(DATA_DIRECTORY, 'precompute.json')

    # Load the words from the respective files
    guesses = load_words(GUESSES_PATH)
    answers = load_words(ANSWERS_PATH)

    # Initialize a hashmap to store the colorings
    colouring_hashmap = {}
    
    # Iterate through each guess to calculate possible colorings
    for i, guess in enumerate(guesses):
        # Clear terminal and show progress every 10%
        if i != 0 and i % (len(guesses) // 70) == 0:
            clear_terminal()
            print(f"Creating precompute.json | Progress: {i / len(guesses):.3%}")

        # Dictionary to store the colorings for the current guess
        possible_colourings = {}
        for solution in answers:
            colouring = get_tile_colouring(guess, solution)  # Get the coloring for this guess-solution pair
            possible_colourings[solution] = colouring  # Store the coloring in the dictionary

        # Store the dictionary of colorings in the main hashmap
        colouring_hashmap[guess] = possible_colourings
    
    print(f"Saving precompute.json ⏳")
    # Write the hashmap to the precompute JSON file
    with open(PRECOMPUTE_PATH, 'w') as json_file:
        json.dump(colouring_hashmap, json_file, indent=4)  # Write with indentation for readability
        print("precompute.json saved ✅")  # Indicate that the file creation is complete