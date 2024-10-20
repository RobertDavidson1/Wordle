import os 
import json
import platform
import numpy as np
from collections import defaultdict

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


def getTransitionInfo(state, action, colouringArray):
    # takes a state (a tuple of indices of words) and an action (an index of a word)
    # returns a dictionary with keys as the possible next states and values as the probability of transitioning to that state
    
    # state is a tuple of indices of words
    stateLen = state.size

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
