import json
from tqdm import tqdm
import numpy as np
from src.gameTree.helperFunctions import loadWords, getTileColouring

def createPrecomputeBinary():
    # Load the list of words
    words = loadWords()
    N = len(words)

    # Create a dictionary mapping each word to its index
    wordIndices = {word: idx for idx, word in enumerate(words)}

    # Initialize a 2D numpy array to store the colouring codes
    colouringArray = np.zeros((N, N), dtype=np.uint8)

    # Iterate over each pair of words to compute the colouring codes
    for i, guess in enumerate(tqdm(words)):
        for j, solution in enumerate(words):
            # Get the colouring code for the current guess and solution pair
            coloring_code = getTileColouring(guess, solution)
            # Store the colouring code in the array
            colouringArray[i, j] = coloring_code

    # Save the colouring array to a binary file
    np.save("../data/precomputeData/precompute.npy", colouringArray)
    
    # Save the word-index mapping to a JSON file
    with open("../data/precomputeData/word_indices.json", "w") as f:
        json.dump(wordIndices, f)

if __name__ == "__main__":
    createPrecomputeBinary()