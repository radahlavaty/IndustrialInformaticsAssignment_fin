from enum import Enum


class PalletStatus(Enum):
    MOVING_TO_Z2 = 1
    MOVING_TO_Z3 = 2
    MOVING_TO_Z4 = 3
    MOVING_TO_Z5 = 4
    DRAWING = 5
    WAIT_PEN_CHANGE = 6
    WAITING = 7
    WAIT_FOR_REMOVAL = 8
    WAIT_FOR_MOVING = 9
