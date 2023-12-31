from enum import Enum

class TransformEnum(Enum):
    PASS = 0
    FILL_AVG = 1
    STR_NONE = 2
    STR_NORMAL = 3
    FORCE_ONE = 4
    DATE_FROM = 5
    FILL_CERO = 6
    STR_NO = 7
    STR_UNKNOWN = 8


class Transform():
    def __init__(self, transformEnum: TransformEnum, column_base: str = "") -> None:
        self.transformEnum = transformEnum
        self.column_base = column_base


def transform_N_T_S_M_V(x):
    if x.upper() == "NONE":
        return 0
    elif x.upper() == "TRACES":
        return 1
    elif x.upper() == "SLIGHT":
        return 2
    elif x.upper() == "MODERATE":
        return 3
    elif x.upper() == "SEVERE":
        return 4


def transform_E_N_L(x):
    if x.upper() == "EARLY":
        return 0
    elif x.upper() == "NORMAL":
        return 1
    elif x.upper() == "LATE":
        return 2


def transform_Y_N(x):
    if x.upper() == "YES":
        return 1
    elif x.upper() == "NO":
        return 0


def transform_Y_N_U(x):
    if x.upper() == "YES":
        return 1
    elif x.upper() == "NO":
        return -1
    elif x.upper() == "UNKNOWN":
        return 0