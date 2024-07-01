import os
import platform
import json

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
    with open(precompute_full_path, "r") as file:
        data = json.load(file)
    return data