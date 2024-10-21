# game_tree/tree_node.py

import numpy as np

class TreeNode:
    def __init__(self, state: np.ndarray, depth: int, value: float = None, best_action: str = None):
        """
        Represents a node in the game tree.

        Parameters:
        - state: Current game state as a NumPy array.
        - depth: Current depth in the tree.
        - value: Computed value of the state.
        - best_action: Best action from this state.
        """
        self.state = state
        self.depth = depth
        self.value = value
        self.best_action = best_action
        self.children = {}  # action -> TreeNode

    def __repr__(self):
        return f"TreeNode(depth={self.depth}, value={self.value}, best_action={self.best_action})"
