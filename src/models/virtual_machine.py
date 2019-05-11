import struct
from typing import List

from models.memory import Memory
from models.register import Register
from models.stack import Stack


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

    def prepare_code(self, source_file):
        pass

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
