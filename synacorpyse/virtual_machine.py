import struct
import sys
from typing import List

from synacorpyse.constants import Action
from synacorpyse.memory import Memory
from synacorpyse.register import Register
from synacorpyse.stack import Stack
from synacorpyse.token import Tokens

real_time_output = False
vm_super_logs = False


class VirtualMachine:
    @property
    def actions(self):
        return {
            Action.update_register: self.write_register,
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
    def registers(self) -> List[Register]:
        return self.__registers

    def write_register(self, address, value):
        if vm_super_logs:
            print(f'write register address: {address}')
            print(f'write register value: {value}')
        self.__registers[address].value = value
        if vm_super_logs:
            print(self.__registers[address])
        self.memory.set_next()

    def read_register(self, address):
        return self.__registers[address].value

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
        self.__memory = Memory()
        self.__output = ''

    @staticmethod
    def init_registers(num_regs):
        return [Register(address=address) for address, _ in enumerate(range(num_regs))]

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

    def set(self, address, value):
        self.__registers[address].value = value
        self.memory.set_next()

    def push_stack(self, value):  # Push the value of the token only.  Address is irrelevant.
        if vm_super_logs:
            print('push stack')
        self.stack.push(value)
        return self.memory.set_next()

    def pop_stack(self, address):
        if vm_super_logs:
            print('pop stack')
        value = self.stack.pop()
        self.write_register(address, value)
        return self.memory.set_next()

    def read_memory(self, address, memory_address):
        if vm_super_logs:
            print('read memory vm')
        mem_val = self.memory.read(memory_address)
        if vm_super_logs:
            print(f'reg num: {address}')
            print(f'memory address: {memory_address}')
            print(f'mem val: {mem_val}')
        self.write_register(address, mem_val)
        # self.__registers[address].value = mem_val
        # self.memory.write(address, mem_val)

        return self.memory.set_next()

    def write_memory(self, target, token):
        if vm_super_logs:
            print('write memory')
            print(target)
            print(token)
        self.memory.write(target, token)
        return self.memory.set_next()

    def update_display(self, ascii_code):
        if real_time_output:
            print(chr(ascii_code.value), end='')
        self.output += chr(ascii_code.value)
        return self.memory.set_next()

    def jump(self, destination):
        if vm_super_logs:
            print('jump')
            print(f'destination: {destination}')
        return self.memory.set_next(destination)

    def halt(self):
        if vm_super_logs:
            print('halt')
        return self.memory.set_next(-1)

    def call(self, current_address, destination):
        if vm_super_logs:
            print('call')
        self.stack.push(current_address + 2)
        return self.memory.set_next(destination)

    def ret(self):
        if vm_super_logs:
            print('ret')
        destination = self.stack.pop()
        return self.memory.set_next(destination)

    def no_op(self):
        return self.memory.set_next()

    def load(self, source_file):
        input_values = self.interpret_binary(source_file)
        tokenizer = Tokens(input_values)
        tokens = [token for token in tokenizer]
        self.memory.load(tokens)

    def run(self):
        while True:
            try:
                token = self.memory.current_token()
                if token.type != 'COMMAND':
                    self.memory.set_next()
                    continue

                args = self.get_args(token)
                operation = token.operation(*args)
                execute_action = operation.operate(token.address, self.callback)
                execute_action()
                if vm_super_logs:
                    print(self.memory.position)
                if self.memory.position == -1:
                    break
            except Exception as ex:
                print('You fucked up.')
                print(ex)
                print(f'current token: {token}')
                print(f'current args: {args}')
                print(self.output)
                raise ex
        print('Finished.')
        print(self.output)
        sys.exit()

    def process(self, memory_navigator):
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
