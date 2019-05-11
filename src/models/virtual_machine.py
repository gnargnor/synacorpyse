from typing import List

from models.register import Register
from models.stack import Stack


class VirtualMachine:
    __registers = None

    def __init__(self, num_regs):
        self.registers: List[Register] = self.create_registers(num_regs)
        self.stack: Stack = self.create_stack()

    @staticmethod
    def create_registers(num_regs):
        return [Register(address=address) for address, _ in enumerate(range(num_regs))]

    @staticmethod
    def create_stack():
        return Stack()
