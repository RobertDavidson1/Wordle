**(Not finished)**
**Solves in an AVG of 3.421**
- Algorithm credit : <a href="http://wordle-page.s3-website-us-east-1.amazonaws.com/assets/Wordle_Paper_Final.pdf">Link</a>
- Tied fastest Wordle Solving algorithm
- Uses different starting word to original paper (Tarse vs Salet)
- Trains faster than the original paper: Takes ~ 1 hour on 8 cores vs "days in C++ implementation across 64 cores"
___

![Web](imgs/image.png)
___
# How to use:
**To use the GUI:**
- Run src/main.py to start a Flask server.
- Enter the returned color codes to get the optimal word.

**To auto-solve today's Wordle:**
- Run src/AutoSolveBot.py.
- This script uses Selenium to automatically solve the Wordle puzzle for the day.
