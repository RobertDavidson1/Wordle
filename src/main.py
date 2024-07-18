import os
from data_initializer import ensure_data_exists
from flask_app import create_app
from decision_tree import build_and_save_tree

def main():
    
    game_solved = ensure_data_exists()

    if not game_solved:
        build_and_save_tree()
    
    app = create_app()
    app.run(debug=True)

if __name__ == "__main__":
    main()
