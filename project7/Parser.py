from unittest import case
import os
from Command_Type import CommandType

class Parser:
   def __init__(self, filename):
    self.file = filename
    self.reader = open(filename, 'r')
    self.instruction = ""
    self.type_of_command = None

   def has_more_lines(self):
       try:

           pos = self.reader.tell()
           char = self.reader.read(1)
           self.reader.seek(pos)
           return bool(char)

       except IOError as e:
           raise IOError(f"Can't read from the file {e}")

   def advance(self):
    if self.has_more_lines():

           self.instruction = self.reader.readline()
           self.instruction = self.instruction.strip()
           #print(self.instruction)

           while self.instruction == '\n' or self.instruction.startswith('/'):
                 self.instruction = self.reader.readline()
                 #print(self.instruction)

           self.type_of_command = CommandType.check_type(self.instruction.split()[0:1][0])

    else:
        print("No more lines")

   def command_type(self):
        return self.type_of_command

   def arg1(self):
       match self.type_of_command:
           case CommandType.C_POP:
               return self.instruction.split()[1:2][0]

           case CommandType.C_PUSH:
               return self.instruction.split()[1:2][0]

           case CommandType.C_ARITHMETIC:
               return self.instruction.split()[0:1][0]


   def arg2(self):
       match self.type_of_command:
           case CommandType.C_POP:
               return self.instruction.split()[2:3][0]

           case CommandType.C_PUSH:
               return self.instruction.split()[2:3][0]

           case CommandType.C_ARITHMETIC:
               pass
