import os
import sys
import shutil
from Parser import *
from CodeWriter  import *
from Command_Type import *

def main():
    # print("Input name of file")
    #filename = input()
    filename = sys.argv[1]

    if os.path.isdir(filename):

        dir_name = os.path.dirname(filename)
        #print(dir_name)
        output_file = dir_name + ".asm"

        #output_file = os.path.join(filename, dir_name + ".asm")
        #os.rename(".asm", os.path.join(dir_name, dir_name + ".asm"))
        #print(output_file)

        writer = CodeWriter(output_file)

        if output_file in os.listdir(filename):
            os.remove(os.path.abspath(output_file))

        shutil.move(os.path.abspath(output_file), os.path.abspath(filename))

        vm_files = [file for file in os.listdir(filename) if file.endswith('.vm')]
        for file in vm_files:

            parser = Parser(os.path.join(filename, file))
            while parser.has_more_lines():
                parser.advance()
                writer.write_command(parser.instruction)
                if parser.command_type() == CommandType.C_ARITHMETIC:
                    # print(parser.arg1())
                    writer.write_arithmetic(parser.arg1())
                else:
                    # print(parser.command_type(), parser.arg1(), parser.arg2())
                    writer.write_push_pop(parser.command_type(), parser.arg1(), parser.arg2())

        writer.close()

    elif filename.endswith('.vm'):
        parser = Parser(filename)
        output_file = filename[:-2] + "asm"
        writer = CodeWriter(output_file)
        while parser.has_more_lines():
            parser.advance()
            writer.write_command(parser.instruction)
            if parser.command_type() == CommandType.C_ARITHMETIC:
                # print(parser.arg1())
                writer.write_arithmetic(parser.arg1())
            else:
                # print(parser.command_type(), parser.arg1(), parser.arg2())
                writer.write_push_pop(parser.command_type(), parser.arg1(), parser.arg2())
        writer.close()

    else:
        print("Invalid input")

if __name__ == '__main__':
    main()


