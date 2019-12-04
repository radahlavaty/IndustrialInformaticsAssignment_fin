from enum import Enum


class Events(Enum):
    Z1_CHANGED = "Z1_Changed"
    Z2_CHANGED = "Z2_Changed"
    Z3_CHANGED = "Z3_Changed"
    Z4_CHANGED = "Z4_Changed"
    Z5_CHANGED = "Z5_Changed"
    PEN_CHANGE_STARTED = "PenChangeStarted"
    PEN_CHANGE_ENDED = "PenChangeEnded"
    DRAW_START_EXECUTION = "DrawStartExecution"
    DRAW_END_EXECUTION = "DrawEndExecution"


class PalletStatus(Enum):
    MOVING_TO_Z2 = 1
    MOVING_TO_Z3 = 2
    MOVING_TO_Z4 = 3
    MOVING_TO_Z5 = 4
    DRAWING = 5
    WAITING = 6


class PhoneColor(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class PhoneShape(Enum):
    FRAME_1 = "Draw1"
    FRAME_2 = "Draw2"
    FRAME_3 = "Draw3"
    SCREEN_1 = "Draw4"
    SCREEN_2 = "Draw5"
    SCREEN_3 = "Draw6"
    KEYBOARD_1 = "Draw7"
    KEYBOARD_2 = "Draw8"
    KEYBOARD_3 = "Draw9"


class StatusCode(Enum):
    WORKING = 1
    ERROR = 2
    IDLE = 3


class Zone(Enum):
    Z1 = 1
    Z2 = 2
    Z3 = 3
    Z4 = 4
    Z5 = 5
