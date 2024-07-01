from data_initializer import ensure_data_exists
from helpers import load_words, load_colouring
import os

if __name__ == "__main__":
    ensure_data_exists()

    DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'data',)
    GUESSES_PATH = os.path.join(DATA_DIRECTORY, 'allowed_guesses.txt')
    PRECOMPUTE_PATH = os.path.join(DATA_DIRECTORY, 'precompute.json')

    guesses = load_words(GUESSES_PATH)
    precomputed_colouring = load_colouring(PRECOMPUTE_PATH)
    
    