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
    COORDINATE_DECIMAL = 9
    COORDINATE_DECIMAL_LIMIT_180 = 10


class Transform():
    def __init__(
            self, 
            transformEnum: TransformEnum, 
            column_base: str = "", 
            column_coordinate_degree: str = "",
            column_coordinate_minute: str = "",
            column_coordinate_NSEW: str = "",
        ) -> None:
        self.transformEnum = transformEnum
        self.column_base = column_base
        self.column_coordinate_minute = column_coordinate_minute
        self.column_coordinate_NSEW = column_coordinate_NSEW
        self.column_coordinate_degree = column_coordinate_degree


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
    
def transform_N_S_W_E(x):
    if x.upper() == "N":
        return 1
    elif x.upper() == "S":
        return -1
    elif x.upper() == "W":
        return -1
    elif x.upper() == "E":
        return 1