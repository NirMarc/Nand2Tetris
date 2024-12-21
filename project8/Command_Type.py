from enum import Enum

class CommandType(Enum):
    C_PUSH = "push"
    C_POP = "pop"
    C_ARITHMETIC = "arithmetic"
    C_LABEL = "label"
    C_GOTO = "goto"
    C_IF = "if-goto"
    C_FUNCTION = "function"
    C_CALL = "call"
    C_RETURN = "return"

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
            case "label":
                return CommandType.C_LABEL
            case "if-goto":
                return CommandType.C_IF
            case "goto":
                return CommandType.C_GOTO
            case "function":
                return CommandType.C_FUNCTION
            case "call":
                return CommandType.C_CALL
            case "return":
                return CommandType.C_RETURN

