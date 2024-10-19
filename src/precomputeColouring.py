import json
from tqdm import tqdm
import numpy as np
from helperFunctions import loadWords, getTileColouring



def createPrecomputeBinary():
    words = loadWords()
    N = len(words)
    word_to_index = {word: idx for idx, word in enumerate(words)}

    colouringArray = np.zeros((N, N), dtype=np.uint8)

    for i, guess in enumerate(tqdm(words)):
        for j, solution in enumerate(words):
            coloring_code = getTileColouring(guess, solution)
            colouringArray[i, j] = coloring_code

    np.save("../data/precomputeData/precompute.npy", colouringArray)
    
    with open("../data/precomputeData/word_indices.json", "w") as f:
        json.dump(word_to_index, f)