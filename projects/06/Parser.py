"""
Functionalities:
1. Get rid of all spaces and comments.
2. Read assembly commands and take them down.
"""


class Parser:
    def __init__(self, file_path):

        self.asm_codes = []
        self.current_line = 0
        self.current_command = ''

        # Remove all spaces and comments
        with open(file_path, 'r') as file:
            for line in file:
                _line = line.strip()
                if len(_line) == 0 or _line[0] == '/':
                    continue
                if _line.find('/') != -1:
                    _line = _line[:_line.find('/')]
                self.asm_codes.append(_line.strip())
        self.asm_codes.append('#END')   # flag of end

    def hasMoreCommands(self):
        if self.current_line == 0 and len(self.asm_codes) != 0:
            self.current_command = self.asm_codes[0]
            return True
        elif self.current_line != len(self.asm_codes) - 1:
            return True
        else:
            self.current_line = 0
            return False

    def advance(self):
        if self.hasMoreCommands():
            self.current_line += 1
            self.current_command = self.asm_codes[self.current_line]

    def commandType(self):
        """
        The return value contains 3 types:
        1. A_Command. Starts with '@'.
        2. C_Command. Includes dest, comp, jump three fileds.
        3. L_Command. Starts with '(', the label line.
        """
        if self.current_command[0] == '@':   # A_Command
            return 'A'
        elif self.current_command[0] == '(':  # L_Command
            return 'L'
        else:
            return 'C'

    def symbol(self):
        """
        Only be called when CommandType() is 'A' or 'L',
        which means the command likes '@xxx' or '(xxx)'.
        If '(xxx)', returns 'xxx';
        If '@xxx', returns decimal number xxx(to string) or a symbol 'xxx'
        """
        if self.commandType() == 'L':
            return self.current_command[1:-1]
        elif self.commandType() == 'A':
            if self.current_command[1:].isdigit():
                return str(self.current_command[1:])
            else:
                return self.current_command[1:]

    def dest(self):
        """
        Only be called when commandType is 'C'.
        A 'C' command is like 'dest = comp; jump',
        any of the three fields is optional.
        """
        if self.commandType() == 'C':
            if self.current_command.find('=') != -1:
                return self.current_command[0:self.current_command.find('=')]
            else:
                return ''

    def comp(self):
        if self.commandType() == 'C':
            if self.current_command.find('=') != -1 and self.current_command.find(';') != -1:
                return self.current_command[self.current_command.find('=') + 1: self.current_command.find(';')]
            elif self.current_command.find(';') != -1:
                return self.current_command[0:self.current_command.find(';')]
            elif self.current_command.find('=') != -1:
                return self.current_command[self.current_command.find('=') + 1:]
            else:
                return ''

    def jump(self):
        if self.commandType() == 'C':
            if self.current_command.find(';') != -1:
                return self.current_command[self.current_command.find(';') + 1:]
            else:
                return ''
