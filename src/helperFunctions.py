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


def getTransitionInfo(state: list[str], action: str, colouringArray: np.ndarray ,wordIndices: dict) -> dict:
    # Convert 'action' to its index
    action_idx = wordIndices.get(action)
    if action_idx is None:
        raise ValueError(f"Action word '{action}' not found in wordIndices.")
    
    state_indices = [wordIndices.get(word) for word in state]
    state_indices = [idx for idx in state_indices if idx is not None]
    
    if not state_indices:
        raise ValueError("No valid solutions in the state.")

    state_indices_array = np.array(state_indices, dtype=int)
    
    colorings = colouringArray[action_idx, state_indices_array]
    
    unique_colorings, counts = np.unique(colorings, return_counts=True)
    
    probabilities = counts / len(state_indices)
    
    transitionInfo = {int(coloring): float(prob) for coloring, prob in zip(unique_colorings, probabilities)}
    
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
