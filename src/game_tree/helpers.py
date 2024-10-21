import os 
import json
import numpy as np
from collections import defaultdict


def loadWords() -> list[str]:
    """
    Loads words from the 'wordsList.txt' file located in the 'data' directory.

    Returns:
    - List of words.
    """
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the absolute path to the data directory
    data_dir = os.path.join(script_dir, '..', '..', 'data')
    
    # Path to wordsList.txt
    words_file_path = os.path.join(data_dir, 'wordsList.txt')
    
    if not os.path.exists(words_file_path):
        raise FileNotFoundError(f"Words file not found at: {words_file_path}")
    
    with open(words_file_path, "r") as file_handle:
        wordList = [word.strip() for word in file_handle]
    
    return wordList


def loadColouring() -> tuple[np.ndarray, dict]:
    """
    Loads colouring data and word indices from the 'precomputeData' directory.

    Returns:
    - colouringArray: NumPy array of colouring information.
    - wordIndices: Dictionary mapping words to indices.
    """
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the absolute path to the precomputeData directory
    precompute_dir = os.path.join(script_dir, '..', '..', 'data', 'precomputeData')
    
    # Paths to precompute.npy and word_indices.json
    precompute_file_path = os.path.join(precompute_dir, 'precompute.npy')
    word_indices_file_path = os.path.join(precompute_dir, 'word_indices.json')
    
    # Check if files exist
    if not os.path.exists(precompute_file_path):
        raise FileNotFoundError(f"Precompute file not found at: {precompute_file_path}")
    if not os.path.exists(word_indices_file_path):
        raise FileNotFoundError(f"Word indices file not found at: {word_indices_file_path}")
    
    # Load colouringArray
    colouringArray = np.load(precompute_file_path)
    
    # Load wordIndices
    with open(word_indices_file_path, "r") as f:
        wordIndices = json.load(f)
    
    return colouringArray, wordIndices

def getTransitionInfo(state, action, colouringArray, stateLen):
    # takes a state (a tuple of indices of words) and an action (an index of a word)
    # returns a dictionary with keys as the possible next states and values as the probability of transitioning to that state
    
 

    # group the words in the state by their colouring
    grouped_words = defaultdict(list)

    # iterate over all possible solutions
    for possibleSolution in state:
        # get the colouring of the tile
        tileColouring = colouringArray[action, possibleSolution]
        # append the solution to the list of words with the same colouring
        grouped_words[tileColouring].append(possibleSolution)

    transitionInfo = {}
    for words in grouped_words.values():
        probability = len(words) / stateLen
        transitionInfo[tuple(words)] = probability

    return transitionInfo

def getTileColouring(guess, solution):
    result = 0
    multiplier = 1
    solution_counts = {}

    for char in solution:
        solution_counts[char] = solution_counts.get(char, 0) + 1

    # First pass for greens
    for i in range(len(guess)):
        if guess[i] == solution[i]:
            result += 2 * multiplier
            solution_counts[guess[i]] -= 1
        multiplier *= 3

    # Second pass for yellows
    multiplier = 1
    for i in range(len(guess)):
        if guess[i] != solution[i]:
            if solution_counts.get(guess[i], 0) > 0:
                result += 1 * multiplier
                solution_counts[guess[i]] -= 1
        multiplier *= 3

    return result

def decode_coloring(coloring_code : int) -> str:
    mapping = {2: 'g', 1: 'y', 0: '-'}
    coloring = ''

    for position in range(5):
        # Extract the least significant digit (base-3)
        rem = coloring_code % 3
        # Get the corresponding coloring character
        coloring += mapping.get(rem, '-')
        # Move to the next digit
        coloring_code //= 3

    return coloring
