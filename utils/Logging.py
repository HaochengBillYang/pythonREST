from enum import Enum


class ColorCode(Enum):
    GREEN = 1
    RED = 2
    BLUE = 3
    YELLOW = 4
    CYAN = 5
    RESET = 99

    def to_code(self) -> str:
        if self == ColorCode.GREEN:
            return "\033[32m"
        elif self == ColorCode.RED:
            return "\033[31m"
        elif self == ColorCode.YELLOW:
            return "\033[33m"
        elif self == ColorCode.CYAN:
            return "\033[35m"
        elif self == ColorCode.BLUE:
            return "\033[36m"
        elif self == ColorCode.RESET:
            return "\033[0m"
        raise "Never Happen"
