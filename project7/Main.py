from os import write
import sys

from Parser import *
from CodeWriter  import *
from Command_Type import *

def main():
    # print("Input name of file")
    #filename = input()
    filename = sys.argv[1]
    # if filename == "exit":
    #     return
    parser = Parser(filename)
    output_file = filename[:-2] + "asm"
    writer = CodeWriter(output_file)

    while parser.has_more_lines():
        parser.advance()
        if parser.command_type() == CommandType.C_ARITHMETIC:
            #print(parser.arg1())
            writer.write_arithmetic(parser.arg1())
        else:
            #print(parser.command_type(), parser.arg1(), parser.arg2())
            writer.write_push_pop(parser.command_type(), parser.arg1(), parser.arg2())

    writer.close()

if __name__ == '__main__':
    main()


