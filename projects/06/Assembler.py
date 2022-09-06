import sys
import os
from Code import Code
from Parser import Parser
from SymbolTable import SymbolTable

"""
Two-pass assembler.
First pass, record all labels into the symboltable.
Second pass, read, parse and translate each line of assembly code to 0s and 1s

Usage:
    > Assembler.py [path of .asm file]
    example: > Assembler.py ./rect/Rect.asm
    (Then there will be a file named 'Rect.hack' in current dir)
"""


def main():
    file_path = sys.argv[1]
    file_name = os.path.basename(file_path)
    suffix = file_name[-3:]
    assert suffix == "asm", "Input file's name should be 'xxx.asm'!"

    asm = Parser(file_path)

    first_pass(asm)
    binary_codes = second_pass(asm)

    binary_filename = file_name[:-4] + '.hack'
    with open(binary_filename, 'w') as file:
        for line in binary_codes:
            file.write(line + '\n')


def first_pass(asm):
    line_number = 0
    while (asm.hasMoreCommands()):
        if asm.commandType() != 'L':
            line_number += 1
        else:
            SymbolTable.addEntry(asm.symbol(), line_number)
        asm.advance()


def second_pass(asm):
    var_address = 16
    binary = ''
    binary_codes = []

    while(asm.hasMoreCommands()):
        if asm.commandType() == 'L':
            asm.advance()
            continue
        elif asm.commandType() == 'A':
            if not(asm.symbol().isdigit()):  # is symbol
                if SymbolTable.contains(asm.symbol()) == None:
                    SymbolTable.addEntry(asm.symbol(), var_address)
                    var_address += 1
                binary = SymbolTable.getAddress(asm.symbol())
            else:
                binary = int(asm.symbol())

            binary = bin(binary)[2:]  # bin(x) is like "0b010100"
            binary = "0" * (16 - len(binary)) + binary
            binary_codes.append(binary)
        elif asm.commandType() == 'C':
            binary = '111'
            if asm.comp() == '':
                binary += '0101010'
            else:
                binary += Code.comp(asm.comp())

            if asm.dest() == '':
                binary += '000'
            else:
                binary += Code.dest(asm.dest())

            if asm.jump() == '':
                binary += '000'
            else:
                binary += Code.jump(asm.jump())
            binary_codes.append(binary)

        asm.advance()
    return binary_codes


if __name__ == '__main__':
    main()
