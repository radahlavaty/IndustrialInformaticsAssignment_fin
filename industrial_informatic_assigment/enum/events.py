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
