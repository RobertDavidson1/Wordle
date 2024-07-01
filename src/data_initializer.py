from typing import NoReturn
import os
import requests
import time

def download_file_if_missing(url, path):
    if not os.path.isfile(path):
        print(f"{os.path.basename(path)} does not exist.")
        print("Downloading..")

        response = requests.get(url, verify=True)
        if response.status_code == 200:
            with open(path + '.tmp', 'w') as file:
                file.write(response.text)
            os.replace(path + '.tmp', path)
            print(f"Downloaded file to {path}\n")
        else:
            print(f"Failed to download {url}\n")
    else:
        print(f"{os.path.basename(path)} exists")
    


def ensure_data_exists() -> NoReturn:

    DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'data',)
    GUESSES_PATH = os.path.join(DATA_DIRECTORY, 'allowed_guesses.txt')
    ANSWERS_PATH = os.path.join(DATA_DIRECTORY, 'allowed_answers.txt')
    PRECOMPUTE_PATH = os.path.join(DATA_DIRECTORY, 'precompute.json')

    GUESSES_URL = "https://raw.githubusercontent.com/RobertDavidson1/Wordle/main/data/allowed_guesses.txt"
    ANSWERS_URL = "https://raw.githubusercontent.com/RobertDavidson1/Wordle/main/data/allowed_answers.txt"



    if not os.path.isdir(DATA_DIRECTORY):
        print("Data folder does not exist.")
        print("Creating..")
        os.makedirs(DATA_DIRECTORY)
        print("Data folder created\n")
    else:
        print("Data folder exists")
    time.sleep(1)
    
    download_file_if_missing(GUESSES_URL, GUESSES_PATH)
    time.sleep(1)
    
    download_file_if_missing(ANSWERS_URL, ANSWERS_PATH)
    time.sleep(1)

    if not os.path.isfile(PRECOMPUTE_PATH):
        print("\nprecompute.json does not exist")
        if os.path.isfile(os.path.join(os.path.dirname(__file__), 'precompute.py')):
            print("Creating precompute.json..")
            time.sleep(3)
            from precompute import create_precompute_json
            create_precompute_json(DATA_DIRECTORY)
        else:
            print("precompute.py is missing.")
            print("Please redownload from github")
    else:
        print("precompute.json exists")
        time.sleep(1)
        
ensure_data_exists()

        
    