import numpy as np
from dataclasses import dataclass

@dataclass
class Uniform:
    lower: float
    upper: float
    def __call__(self) -> float:
        return np.random.uniform(self.lower, self.upper)