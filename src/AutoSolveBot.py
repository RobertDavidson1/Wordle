import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def color_string(s):
    green_square = '\033[38;2;108;169;101m\033[48;2;108;169;101m⬜\033[0m'
    yellow_square = '\033[38;2;200;182;83m\033[48;2;200;182;83m⬜\033[0m'
    gray_square = '\033[38;2;120;124;127m\033[48;2;120;124;127m⬜\033[0m'

    mapping = {'g': green_square, '-': gray_square, 'y': yellow_square}

    return ''.join(mapping.get(char, char) for char in s)

def play_wordle(strategy):
    # Set up WebDriver options
    options = Options()
    options.add_argument("--start-maximized")
    # Uncomment the line below to run the browser in headless mode
    # options.add_argument("--headless")

    # Initialize WebDriver
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.nytimes.com/games/wordle/index.html")
    time.sleep(2)  # Wait for the page to load

    # Handle the privacy preference pop-up if present
    try:
        # Wait for the pop-up to appear
        time.sleep(1)
        # Find the 'Accept all' button using its data-testid attribute
        accept_all_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="Accept all-btn"]')
        accept_all_button.click()
        print(f"Privacy preference pop-up closed. ✔️")
    except NoSuchElementException:
        print("Privacy preference pop-up not found.")
        pass

    # Handle the welcome screen with the 'Play' button
    try:
        time.sleep(1)
        play_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="Play"]')
        play_button.click()
        print(f"Welcome screen 'Play' button clicked. ✔️")
    except NoSuchElementException:
        print("Welcome screen 'Play' button not found.")
        pass

    # Close the game instructions modal if present
    try:
        time.sleep(1)
        close_button = driver.find_element(By.CLASS_NAME, "Modal-module_closeIcon__TcEKb")
        close_button.click()
        print(f"Game instructions modal closed. ✔️")
    except NoSuchElementException:
        print("Game instructions modal not found.")
        pass

    time.sleep(1)

    # Start playing
    current_strategy = strategy
    for attempt in range(6):
        # Get the best word to guess
        word = current_strategy["best word"]
        print(f"\nAttempt {attempt + 1}: {word.upper()}")

        # Enter the word into the game
        for letter in word:
            letter = letter.lower()
            key = driver.find_element(By.CSS_SELECTOR, f'button[data-key="{letter}"]')
            key.click()
            time.sleep(0.1)

        # Press Enter
        enter_key = driver.find_element(By.CSS_SELECTOR, 'button[data-key="↵"]')
        enter_key.click()
        time.sleep(3)  # Wait for the animation to complete

        # Read the coloring of the tiles
        row_selector = f'div[class*="Row-module_row__"][aria-label="Row {attempt + 1}"]'
        row = driver.find_element(By.CSS_SELECTOR, row_selector)
        tiles = row.find_elements(By.CSS_SELECTOR, 'div[class*="Tile-module_tile__"]')

        pattern = ''
        for tile in tiles:
            evaluation = tile.get_attribute('data-state')  # 'correct', 'present', 'absent'
            if evaluation == 'correct':
                pattern += 'g'
            elif evaluation == 'present':
                pattern += 'y'
            elif evaluation == 'absent':
                pattern += '-'
            else:
                pattern += '?'
        
        coloured_string = color_string(pattern)
        print(f"Pattern: {coloured_string}")

        # Check if the word is correct
        if pattern == 'ggggg':
            print("\n Wordle solved! ✔️")
            break

        # Update the strategy
        if "next states" in current_strategy and pattern in current_strategy["next states"]:
            current_strategy = current_strategy["next states"][pattern]
        else:
            print("Pattern not found in strategy. Cannot proceed.")
            break

    time.sleep(5)  # Keep the browser open for a short while to see the result
    driver.quit()

# Load the strategy from '../data/decision_tree.json'
with open('../data/decision_tree.json', 'r') as file:
    wordle_strategy = json.load(file)

print("""


██╗    ██╗ ██████╗ ██████╗ ██████╗ ██╗     ███████╗             
██║    ██║██╔═══██╗██╔══██╗██╔══██╗██║     ██╔════╝             
██║ █╗ ██║██║   ██║██████╔╝██║  ██║██║     █████╗               
██║███╗██║██║   ██║██╔══██╗██║  ██║██║     ██╔══╝               
╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝███████╗███████╗             
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝             
                                                                
███████╗ ██████╗ ██╗    ██╗   ██╗███████╗██████╗                
██╔════╝██╔═══██╗██║    ██║   ██║██╔════╝██╔══██╗               
███████╗██║   ██║██║    ██║   ██║█████╗  ██████╔╝               
╚════██║██║   ██║██║    ╚██╗ ██╔╝██╔══╝  ██╔══██╗               
███████║╚██████╔╝███████╗╚████╔╝ ███████╗██║  ██║               
╚══════╝ ╚═════╝ ╚══════╝ ╚═══╝  ╚══════╝╚═╝  ╚═╝               
                                                                
                ██████╗ ██╗   ██╗                               
                ██╔══██╗╚██╗ ██╔╝                               
                ██████╔╝ ╚████╔╝                                
                ██╔══██╗  ╚██╔╝                                 
                ██████╔╝   ██║                                  
                ╚═════╝    ╚═╝                                  
                                                                
            ██████╗  ██████╗ ██████╗                            
            ██╔══██╗██╔═══██╗██╔══██╗                           
            ██████╔╝██║   ██║██████╔╝                           
            ██╔══██╗██║   ██║██╔══██╗                           
            ██║  ██║╚██████╔╝██████╔╝                           
            ╚═╝  ╚═╝ ╚═════╝ ╚═════╝                            

                       
""")


# Run the bot
play_wordle(wordle_strategy)
