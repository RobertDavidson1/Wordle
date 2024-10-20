import os 
import json
import platform
import numpy as np

def loadWords() -> list[str]:
    abs_file_path = os.path.abspath("../data/wordsList.txt")
    
    with open(abs_file_path, "r") as file_handle:
        wordList = [word.strip() for word in file_handle]

    return wordList


def loadColouring() -> dict:
    colouringArray = np.load("../data/precomputeData/precompute.npy")
    with open("../data/precomputeData/word_indices.json", "r") as f:
        wordIndices = json.load(f)
    
    return colouringArray, wordIndices


def getTransitionInfo(state: list[str], action: str, colouringArray: np.ndarray, wordIndices: dict) -> dict:
    from collections import defaultdict

    # Initialize a defaultdict to group words by their coloring
    grouped_words = defaultdict(list)
    state_len = len(state)

    # Convert 'action' to its index
    action_idx = wordIndices.get(action)
    if action_idx is None:
        raise ValueError(f"Action word '{action}' not found in wordIndices.")

    # Iterate over each possible solution in the state
    for possibleSolution in state:
        solution_idx = wordIndices.get(possibleSolution)
        if solution_idx is None:
            # Optionally, log or handle words not found in wordIndices
            continue
        # Retrieve the coloring code from the coloring array
        tileColouring = colouringArray[action_idx, solution_idx]
        # Group the word by its coloring code
        grouped_words[tileColouring].append(possibleSolution)

    # Construct the transitionInfo dictionary
    # Keys: Tuples of words sharing the same coloring
    # Values: Probability of that coloring occurring
    transitionInfo = {}
    for coloring_code, words in grouped_words.items():
        probability = len(words) / state_len
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
