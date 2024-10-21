# game_tree/params.py

from dataclasses import dataclass, field
import numpy as np


@dataclass
class GlobalParams:
    allActions: np.ndarray
    colouringArray: np.ndarray
    stateCache: dict = field(default_factory=dict)