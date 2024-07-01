from data_initializer import ensure_data_exists
from helpers import load_words, load_colouring
import os
import multiprocessing


if __name__ == "__main__":
    ensure_data_exists()

    DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'data',)
    GUESSES_PATH = os.path.join(DATA_DIRECTORY, 'allowed_guesses.txt')
    PRECOMPUTE_PATH = os.path.join(DATA_DIRECTORY, 'precompute.json')

    state = ["setup", "smite", "smote", "spite", "stein", "stern", "stoke", "stone", "store", "stove", "suite"]
    guesses = load_words(GUESSES_PATH)
    precomputed_colouring = load_colouring(PRECOMPUTE_PATH)

    manager = multiprocessing.Manager()
    shared_guessed = manager.list(guesses)
    shared_precomputed_colouring = manager.dict(precomputed_colouring)
