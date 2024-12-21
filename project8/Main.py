import os
import sys
from Parser import *
from CodeWriter  import *
from Command_Type import *

class Main:

    @staticmethod
    def main():
        filename = sys.argv[1]

        if os.path.isdir(filename):

            dir_name = os.path.basename(filename)

            output_file = os.path.join(filename, dir_name + ".asm")


            writer = CodeWriter(output_file)
            writer.write_init()
            vm_files = sorted([file for file in os.listdir(filename) if file.endswith('.vm')])

            for file in vm_files:
                writer.set_filename((file)[:-3])
                parser = Parser(os.path.join(filename, file))
                Main.read_and_write(parser, writer)
            writer.close()

        elif filename.endswith('.vm'):
            parser = Parser(filename)
            output_file = filename[:-2] + "asm"
            writer = CodeWriter(output_file)
            Main.read_and_write(parser, writer)
            writer.close()

        else:
            print("Invalid input")


    @staticmethod
    def read_and_write(parser, writer):
            while parser.has_more_lines():
                parser.advance()
                writer.write_command(parser.instruction)
                match parser.command_type():
                    case CommandType.C_ARITHMETIC:
                        writer.write_arithmetic(parser.arg1())
                    case CommandType.C_POP:
                        writer.write_push_pop(parser.command_type(), parser.arg1(), parser.arg2())
                    case CommandType.C_PUSH:
                         writer.write_push_pop(parser.command_type(), parser.arg1(), parser.arg2())
                    case CommandType.C_LABEL:
                         writer.write_label(parser.arg1())
                    case CommandType.C_GOTO:
                        writer.write_goto(parser.arg1())
                    case CommandType.C_IF:
                        writer.write_if(parser.arg1())
                    case CommandType.C_FUNCTION:
                        writer.write_function(parser.arg1(), parser.arg2())
                    case CommandType.C_CALL:
                        writer.write_call(parser.arg1(), parser.arg2())
                    case CommandType.C_RETURN:
                        writer.write_return()



if __name__ == '__main__':
    Main.main()


