from enum import Enum
from src.config import b, c

class Strategy(Enum):
    ALTRUIST = 0,
    PAROCHIALIST = 1,
    EGOIST = 2    

A_IN_MATRIX = [
    [b-c, b-c, -c],
    [b-c, b-c, -c],
    [b, b, 0],
]

A_OUT_MATRIX = [
    [b-c, -c, -c],
    [b, 0, 0],
    [b, 0, 0],
]