from Command_Type import *

class CodeWriter:
    def __init__(self, filename):
        self.writer = open(filename, "w")
        self.label_count = 0

    def write_arithmetic(self, command):
        match command:
            case "add":
                self.writer.write("@SP\n"
                                  "AM=M-1\n"
                                  "D=M\n"
                                  "A=A-1\n"
                                  "M=D+M\n")
            case "sub":
                self.writer.write("@SP\n"
                                  "AM=M-1\n"
                                  "D=M\n"
                                  "A=A-1\n"
                                  "M=M-D\n")
            case "neg":
                self.writer.write("@SP\n"
                                  "A=M-1\n"
                                  "M=-M\n")
            case "and":
                self.writer.write("@SP\n"
                                  "AM=M-1\n"
                                  "D=M\n"
                                  "A=A-1\n"
                                  "M=D&M\n")
            case "or":
                self.writer.write("@SP\n"
                                  "AM=M-1\n"
                                  "D=M\n"
                                  "A=A-1\n"
                                  "M=D|M\n")
            case "not":
                self.writer.write("@SP\n"
                                  "A=M-1\n"
                                  "M=!M\n")
            case _:
                # self.writer.write("@SP\n"
                #                   "M=M-1\n"
                #                   "A=M\n"
                #                   "D=M\n"
                #                   "A=A-1\n"
                #                   "M=M-D\n"
                #                   "D=M\n"
                #                   f"@LOOP{self.label_count}\n")
                # match command:
                #     case "eq":
                #         self.writer.write("D;JEQ\n")
                #     case "gt":
                #         self.writer.write("D;JGT\n")
                #     case "lt":
                #         self.writer.write("D;JLT\n")
                #
                # self.writer.write("@SP\n"
                #                   "M=M-1\n"
                #                   "A=M\n"
                #                   "M=-1\n"
                #                   f"@END{self.label_count}\n"
                #                   "0;JMP\n"
                #                   f"(LOOP{self.label_count})\n"
                #                   "@SP\n"
                #                   "M=M-1\n"
                #                   "A=M\n"
                #                   "M=0\n"
                #                   f"(END{self.label_count})\n"
                #                   "@SP\n"
                #                   "M=M+1\n")
                self.label_count += 1
                self.writer.write("@SP\n"
                                  "AM=M-1\n"
                                  "D=M\n"
                                  "A=A-1\n"
                                  "D=M-D\n"
                                  f"@LOOP{self.label_count}\n")
                match command:
                    case "eq":
                        self.writer.write("D;JEQ\n")
                    case "gt":
                        self.writer.write("D;JGT\n")
                    case "lt":
                        self.writer.write("D;JLT\n")
                self.writer.write("@SP\n"
                                  "A=M-1\n"
                                  "M=0\n"
                                  f"@END{self.label_count}\n"
                                  "0;JMP\n"
                                  f"(LOOP{self.label_count})\n"
                                  "@SP\n"
                                  "A=M-1\n"
                                  "M=-1\n"
                                  f"(END{self.label_count})\n")

    def write_push_pop(self, command, segment, index):
        if command == CommandType.C_PUSH:
          match segment:
              case "constant":
                  self.writer.write(f"@{index}\n"
                                    "D=A\n"
                                    "@SP\n"
                                    "A=M\n"
                                    "M=D\n"
                                    "@SP\n"
                                    "M=M+1\n")
              case "pointer":
                  pointer_index = int(index) + 3
                  self.writer.write(f"@{pointer_index}\n"
                                    "D=M\n"
                                    "@SP\n"
                                    "A=M\n"
                                    "M=D\n"
                                    "@SP\n"
                                    "M=M+1\n")
              case "static":
                  self.writer.write(f"@{self.writer.name}.{index}\n"
                                    "D=M\n"
                                    "@SP\n"
                                    "A=M\n"
                                    "M=D\n"
                                    "@SP\n"
                                    "M=M+1\n")
              case "temp":
                  self.writer.write("@5\n"
                                    "D=A\n"
                                    f"@{index}\n"
                                    "A=D+A\n"
                                    "D=M\n"
                                    "@SP\n"
                                    "A=M\n"
                                    "M=D\n"
                                    "@SP\n"
                                    "M=M+1\n")
              case _:
                  match segment:
                      case "local":
                          self.writer.write("@LCL\n")
                      case "argument":
                          self.writer.write("@ARG\n")
                      case "this":
                          self.writer.write("@THIS\n")
                      case "that":
                          self.writer.write("@THAT\n")
                  self.writer.write("D=M\n"
                                    f"@{index}\n"
                                    "A=D+A\n"
                                    "D=M\n"
                                    "@SP\n"
                                    "A=M\n"
                                    "M=D\n"
                                    "@SP\n"
                                    "M=M+1\n")
        else:
            if segment == "pointer":
                pointer_index = int(index) + 3
                self.writer.write("@SP\n"
                                  "AM=M-1\n"
                                  "D=M\n"
                                  f"@{pointer_index}\n"
                                  "M=D\n")
            elif segment == "static":
                self.writer.write("@SP\n"
                                  "AM=M-1\n"
                                  "D=M\n"
                                  f"@{self.writer.name}.{index}\n"
                                  "M=D\n")
            elif segment == "temp":
                self.writer.write("@5\n"
                                  "D=A\n"
                                  f"@{index}\n"
                                  "D=D+A\n"
                                  "@R13\n"
                                  "M=D\n"
                                  "@SP\n"
                                  "AM=M-1\n"
                                  "D=M\n"
                                  "@R13\n"
                                  "A=M\n"
                                  "M=D\n")
            else:
                match segment:
                  case "local":
                    self.writer.write("@LCL\n")
                  case "argument":
                    self.writer.write("@ARG\n")
                  case "this":
                    self.writer.write("@THIS\n")
                  case "that":
                    self.writer.write("@THAT\n")
                self.writer.write("D=M\n"
                                  f"@{index}\n"
                                  "D=D+A\n"
                                  "@R13\n"
                                  "M=D\n"
                                  "@SP\n"
                                  "AM=M-1\n"
                                  "D=M\n"
                                  "@R13\n"
                                  "A=M\n"
                                  "M=D\n")


    def write_command(self, command):
        self.writer.write("//" + command + "\n")

    def close(self):
        self.writer.close()