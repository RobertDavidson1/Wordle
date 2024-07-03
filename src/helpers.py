import os
import platform
import orjson
import numpy as np

def get_transition_info(state, action, colouring_data):
    new_state = {}
    for word in state:
        colouring = colouring_data[action][word]
        if colouring not in new_state:
            new_state[colouring] = [word]
        else:
            new_state[colouring].append(word)
    transition_info = {tuple(states): (len(states) / len(state)) for states in new_state.values()}
    return transition_info

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

def heuristic_split_and_insert(actions, state, processes, colouring_data):

    # actions = [word for word in actions if word not in state]


    hash = {}
    for guess in actions:
        res = get_transition_info(state, guess, colouring_data)
        hash[guess] = len(res)

    lower_bound = np.percentile(list(hash.values()), 99)

    filtered_words = []

    for word in hash.keys():
        if hash[word] >= lower_bound:
            filtered_words.append(word)

    
    def split_list(words, cpus):
        split_arrays = np.array_split(words, cpus)
        return [list(map(str, sublist)) for sublist in split_arrays]

    sublists = split_list(filtered_words, processes)
    
    return sublists

def heuristic(actions, state, colouring_data):
    hash = {}
    for guess in actions:
        res = get_transition_info(state, guess, colouring_data)
        hash[guess] = len(res)

    lower_bound = np.percentile(list(hash.values()), 95)

    filtered_words = []

    for word in hash.keys():
        if hash[word] >= lower_bound:
            filtered_words.append(word)
    return filtered_words
    