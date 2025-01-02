from enum import Enum
<<<<<<< HEAD
from config import b, c

class Strategy(Enum):
    ALTRUIST = 0,
    PAROCHIALIST = 1,
=======
from src.config import b, c

class Strategy(Enum):
    ALTRUIST = 0
    PAROCHIALIST = 1
>>>>>>> 905479fda059ca2176d60b79ae6a57c67c190a13
    EGOIST = 2    

A_IN_MATRIX = [
    [b-c, b-c, -c],
    [b-c, b-c, -c],
<<<<<<< HEAD
    [b, b, 0],
=======
    [b, b, 0]
>>>>>>> 905479fda059ca2176d60b79ae6a57c67c190a13
]

A_OUT_MATRIX = [
    [b-c, -c, -c],
    [b, 0, 0],
<<<<<<< HEAD
    [b, 0, 0],
=======
    [b, 0, 0]
>>>>>>> 905479fda059ca2176d60b79ae6a57c67c190a13
]