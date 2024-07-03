import multiprocessing
from helpers import load_words, load_colouring, clear_terminal, heuristic_split_and_insert
import os


def recursive_task(individual_list, shared_list, colouring_data, level=0):
    if level > 2:
        return

    if level == 0:
        current_list = individual_list
    else:
        current_list = shared_list

    # Debugging information
    print(f"Process {multiprocessing.current_process().name} at level {level} using list {current_list[:5]}")
    print(f"Colouring {colouring_data['salet']['aback']}")

    # Recursive call
    recursive_task(shared_list, shared_list, colouring_data, level + 1)


def process_task(initial_list, shared_list, colouring_data):
    recursive_task(initial_list, shared_list, colouring_data)
    print(f"Process {multiprocessing.current_process().name} finished.")

if __name__ == "__main__":
    PROCESSES = 5
    DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'data')
    GUESSES_PATH = os.path.join(DATA_DIRECTORY, 'allowed_guesses.txt')
    PRECOMPUTE_PATH = os.path.join(DATA_DIRECTORY, 'precompute.json')
    
    colouring_data = load_colouring(PRECOMPUTE_PATH)
    guesses = load_words(GUESSES_PATH)
    state = ('salet', 'trace')

    # Create a manager to handle shared data
    manager = multiprocessing.Manager()
    
    # Create a shared list and a shared dictionary
    shared_list = guesses
    
    indiv_list = heuristic_split_and_insert(guesses,state,PROCESSES)

    # Create a list to hold references to process objects
    processes = []
    
    # Launch multiple processes
    for i in range(PROCESSES):  # Let's create 5 processes
        p = multiprocessing.Process(target=process_task, args=(indiv_list[i],shared_list, colouring_data))
        processes.append(p)
        p.start()
    
    
    # No need to wait for child processes to complete
    print("Main process does not wait for child processes to finish.")