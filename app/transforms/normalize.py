from enum import Enum

class NormalizeEnum(Enum):
    PASS = 0
    ONE_TO_ONE = 1
    ONE_POSITIVE = 2
    
class Normalize():
    def __init__(self, normalizeEnum: NormalizeEnum) -> None:
        self.normalizeEnum = normalizeEnum