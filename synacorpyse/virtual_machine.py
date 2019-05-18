import struct
import sys
from typing import List

from synacorpyse.constants import Action
from synacorpyse.memory import Memory
from synacorpyse.register import Register
from synacorpyse.stack import Stack
from synacorpyse.token import Tokens

sys.setrecursionlimit(8000)


class VirtualMachine:
    @property
    def actions(self):
        return {
            Action.update_register: self.update_register,
            Action.read_memory: self.read_memory,
            Action.write_memory: self.write_memory,
            Action.update_display: self.update_display,
            Action.push_stack: self.push_stack,
            Action.pop_stack: self.pop_stack,
            Action.call: self.call,
            Action.ret: self.ret,
            Action.no_op: self.no_op,
            Action.jump: self.jump,
            Action.halt: self.halt,
        }

    @property
    def registers(self):
        return self.__registers

    @property
    def memory(self):
        return self.__memory

    @memory.setter
    def memory(self, memory):
        self.__memory = memory

    @property
    def stack(self):
        return self.__stack

    @property  # property is probably not necessary unless validation is needed below
    def output(self):
        return self.__output

    @output.setter
    def output(self, output):
        self.__output = output

    def __init__(self, num_regs: int):
        self.__registers = self.init_registers(num_regs)
        self.__stack = self.init_stack()
        self.__memory = None
        self.__output = ''

    @staticmethod
    def init_registers(num_regs):
        return [Register(reg_num=reg_num) for reg_num, _ in enumerate(range(num_regs))]

    @staticmethod
    def init_stack():
        return Stack()

    def __init_memory(self, tokens):
        self.memory = Memory(tokens)

    def callback(self, message):
        action_type = message.action
        args = message.args

        def execute():
            action = self.actions[action_type]
            action(*args)

        return execute

    def update_register(self, register):
        self.registers[register.reg_num] = register

    def push_stack(self, token):  # Push the value of the token only.  Address is irrelevant.
        self.stack.push(token.value)

    def pop_stack(self, register):
        value = self.stack.pop()
        self.registers[register.reg_num].value = value

    def read_memory(self, register, memory_address):
        memory = self.memory.tokens[memory_address.value]
        self.registers[register.reg_num].value = memory.value

    def write_memory(self, target, source):
        # print(self.memory.tokens[target.value])
        self.memory.tokens[target.value].value = source.value
        # print(self.memory.tokens[target.value])
        # pass

    def update_display(self, ascii_code):
        print(chr(ascii_code.value))
        self.output += chr(ascii_code.value)

    def jump(self, address):
        memory_navigator = self.memory.gen_next(address=address.value)
        return self.process(memory_navigator)

    def halt(self):
        # print(f'output: \n{self.output}')
        # print("HALT")
        sys.exit()

    def call(self, current_address, destination):
        self.stack.push(current_address + 2)
        return self.jump(destination)

    def ret(self):
        destination = self.stack.pop()
        memory_navigator = self.memory.gen_next(address=destination)
        return self.process(memory_navigator)

    def no_op(self):
        pass

    def load(self, source_file):
        input_values = self.interpret_binary(source_file)
        tokenizer = Tokens(input_values)
        tokens = [token for token in tokenizer]
        self.__init_memory(tokens)

    def run(self):
        memory_navigator = self.memory.gen_next(address=0)
        self.process(memory_navigator)

    def process(self, memory_navigator):
        # print()
        for token in memory_navigator:
            if token.type != 'COMMAND':
                continue

            args = self.get_args(token)

            operation = token.operation(*args)

            execute_action = operation.operate(token.address, self.callback)
            execute_action()

    def get_args(self, token):
        args = []
        num_args = token.operation.num_args
        if num_args > 0:
            first_arg = token.address + 1
            args = self.memory.tokens[first_arg:first_arg + num_args]

        # for arg in args:
        #     arg = self.registers[arg.value % 32768] if 32768 <= arg.value <= 32775 else arg

        args = [self.registers[arg.value % 32768]  # replace interpreted value with register value
                if (32768 <= arg.value <= 32775)
                else arg
                for arg in args]
        return args

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
