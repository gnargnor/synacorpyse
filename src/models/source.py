import struct
from typing import List


class SourceFile:
    def __init__(self, source_file: str):
        self.source_file = source_file

    @staticmethod
    def read_bytecode_pair(input_bin):
        pair = 'x'  # placeholder for the `while`
        while pair:
            pair = input_bin.read(2)
            if pair:
                value = struct.unpack('<H', pair)[0]
                yield value

    def interpret_binary(self) -> List[int]:
        with open(self.source_file, 'rb') as input_bin:
            input_values = [value for value in self.read_bytecode_pair(input_bin)]
            return input_values
