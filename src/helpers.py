import os
import platform
import orjson

def clear_terminal():
    current_os = platform.system()
    if current_os == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def load_words(file_path):
    with open(file_path, "r") as file_handle:
        word_array = [word.strip() for word in file_handle]
    return word_array

def load_colouring(file_path):
    base_path = os.path.abspath(os.path.dirname(__file__))
    precompute_full_path = os.path.join(base_path, file_path)
    with open(precompute_full_path, "rb") as file:
        data = orjson.loads(file.read())
    return data

def heuristic_split_and_insert(actions, state, processes):
    # Split the actions list into cpus number of sublists
    def split_list(words, cpus):
        k, m = divmod(len(words), cpus)
        return [words[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(cpus)]

    # Split the actions list
    sublists = split_list(actions, processes)
    
    # Convert the state tuple to a list for manipulation
    temp = list(state)

    # Insert state words into sublists using a round-robin approach
    i = 0
    while temp:
        sublists[i].insert(0, temp.pop())
        i += 1 
        i = i % processes
    
    return sublists