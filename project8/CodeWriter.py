from Command_Type import *

class CodeWriter:
    def __init__(self, filename):
        self.writer = open(filename, "w")
        self.label_count = 0
        self.current_function = "Sys.init"
        self.set_filename(filename)

    def set_filename(self, filename):
        self.filename = filename.split("/")[-1].split("\\")[-1].split(".")[0]

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
                  self.writer.write(f"@{self.filename}.{index}\n"
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
                                  f"@{self.filename}.{index}\n"
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

    def write_label(self, label):
        full_label = f"{self.current_function}${label}"
        self.writer.write(f"({full_label})\n")

    def write_goto(self, label):
        full_label = f"{self.current_function}${label}"
        self.writer.write(f"@{full_label}\n"
                           "0;JMP\n")

    def write_if(self, label):
        full_label = f"{self.current_function}${label}"
        self.writer.write("@SP\n"
                          "AM=M-1\n"
                          "D=M\n"
                          f"@{full_label}\n"
                          "D;JNE\n")

    def write_function(self, function_name, n_vars):
        self.current_function = function_name
        self.writer.write(f"({function_name})\n")

        for _ in range(int(n_vars)):
            self.writer.write("@SP\n"
                              "A=M\n"
                              "M=0\n"
                              "@SP\n"
                              "M=M+1\n")


    def write_call(self, function_name, n_args):
        return_label = f"{self.current_function}$ret.{self.label_count}"
        self.label_count += 1
        self.writer.write(f"@{return_label}\n"
                          "D=A\n"
                          "@SP\n"
                          "A=M\n"
                          "M=D\n"
                          "@SP\n"
                          "M=M+1\n")

        for segment in ["LCL", "ARG", "THIS", "THAT"]:
            self.writer.write(f"@{segment}\n"
                               "D=M\n"
                               "@SP\n"
                               "A=M\n"
                               "M=D\n"
                               "@SP\n"
                               "M=M+1\n")

        self.writer.write("@SP\n"
                          "D=M\n"
                          f"@{(int(n_args) + 5)}\n"
                          "D=D-A\n"
                          "@ARG\n"
                          "M=D\n")

        self.writer.write("@SP\n"
                          "D=M\n"
                          "@LCL\n"
                          "M=D\n")

        self.writer.write(f"@{function_name}\n"
                           "0;JMP\n")

        self.writer.write(f"({return_label})\n")


    def write_return(self):
        self.writer.write("@LCL\n"
                          "D=M\n"
                          "@R13\n"
                          "M=D\n")

        self.writer.write("@5\n"
                          "A=D-A\n" 
                          "D=M\n"
                          "@R14\n" 
                          "M=D\n")

        self.writer.write("@SP\n"
                          "AM=M-1\n"
                          "D=M\n"
                          "@ARG\n"
                          "A=M\n"
                          "M=D\n")

        self.writer.write("@ARG\n"
                          "D=M+1\n"
                          "@SP\n"
                          "M=D\n")


        for i, segment in enumerate(["THAT", "THIS", "ARG", "LCL"]):
            self.writer.write("@R13\n"
                              "D=M\n"
                              f"@{i+1}\n"
                              "A=D-A\n"
                              "D=M\n"
                              f"@{segment}\n"
                              "M=D\n")

        self.writer.write("@R14\n"
                          "A=M\n"
                          "0;JMP\n")


    def write_command(self, command):
        self.writer.write("//" + command + "\n")

    def close(self):
        self.writer.close()

    def write_init(self):
        self.writer.write("@256\n"
                          "D=A\n"
                          "@SP\n"
                          "M=D\n")
        self.write_call("Sys.init", 0)

