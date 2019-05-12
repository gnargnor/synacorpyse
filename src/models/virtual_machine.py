import struct
from typing import List

from models.memory import Memory
from models.register import Register
from models.stack import Stack
from models.token import Tokens


class VirtualMachine:
    @property
    def registers(self):
        return self.__registers

    @property
    def memory(self):
        return self.__memory

    @property
    def stack(self):
        return self.__stack

    def __init__(self, num_regs: int):
        self.__registers = self.init_registers(num_regs)
        self.__memory = self.init_memory()
        self.__stack = self.init_stack()

    @staticmethod
    def init_registers(num_regs):
        return [Register(address=address) for address, _ in enumerate(range(num_regs))]

    @staticmethod
    def init_stack():
        return Stack()

    @staticmethod
    def init_memory():
        return Memory()

    def get_args(self, tokens, cur_address):
        args = []
        num_args = tokens[cur_address].operation.num_args
        print(num_args)
        if num_args > 0:
            first_arg = cur_address + 1
            args = tokens[first_arg:first_arg + num_args]
        args = [self.registers[arg.value % 32768] if (32768 <= arg.value <= 32775) else arg for arg in args]
        return args

    def process(self, tokens, starting_address=0, output=""):
        print()
        print()
        print()
        address = starting_address
        while address < len(tokens):
            token = tokens[address]

            if token.type != 'COMMAND':
                address = address + 1
                continue

            args = self.get_args(tokens, address)
            print()
            print(token)
            print(args)
            operation = token.operation(*args)

            if token.value == 0:
                print(f'output: \n{output}')
                print(f'token: {token.operation}')
                print("HALT")
                operation.operate()

            if token.value == 6:
                destination = operation.operate()
                print(f'jump! token value: {token.value}')
                self.process(tokens=tokens, starting_address=destination, output=output)

            if token.value in [7, 8]:
                destination = operation.operate()
                if destination:
                    print(f'jump! token value: {token.value} destination: {destination}')
                    self.process(tokens=tokens, starting_address=destination, output=output)

            if token.value == 19:
                char = operation.operate()
                output += char

            if token.value == 21:
                operation.operate()

            address += 1

    def run(self, source_file):
        input_values = self.interpret_binary(source_file)
        tokenizer = Tokens(input_values)
        tokens = [token for token in tokenizer]
        self.process(tokens)

    @staticmethod
    def read_bytecode_pair(input_bin):
        pair = 'x'  # placeholder for the `while`
        while pair:
            pair = input_bin.read(2)
            if pair:
                value = struct.unpack('<H', pair)[0]
                yield value

    def interpret_binary(self, source_file) -> List[int]:
        with open(source_file, 'rb') as input_bin:
            input_values = [value for value in self.read_bytecode_pair(input_bin)]
            return input_values
