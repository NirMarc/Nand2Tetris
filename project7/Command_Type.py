from enum import Enum

class CommandType(Enum):
    C_PUSH = "push"
    C_POP = "pop"
    C_ARITHMETIC = "arithmetic"

    def __str__(self):
        return self.value

    @staticmethod
    def check_type(first_arg: str):
        match first_arg:
            case "add":
                return CommandType.C_ARITHMETIC
            case "sub":
                return CommandType.C_ARITHMETIC
            case "neg":
                return CommandType.C_ARITHMETIC
            case "eq":
                return CommandType.C_ARITHMETIC
            case "gt":
                return CommandType.C_ARITHMETIC
            case "lt":
                return CommandType.C_ARITHMETIC
            case "and":
                return CommandType.C_ARITHMETIC
            case "or":
                return CommandType.C_ARITHMETIC
            case "not":
                return CommandType.C_ARITHMETIC
            case "pop":
                return CommandType.C_POP
            case "push":
                return CommandType.C_PUSH

