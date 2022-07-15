from enum import Enum


class Action(Enum):
    CREATE = 1
    ADD_AND_UPDATE = 2
    ADD_ONLY = 3
    UPDATE_ONLY = 4
    OPT_OUT = 5
