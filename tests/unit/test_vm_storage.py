from models.memory import Memory
from models.register import Register
from models.stack import Stack
from models.virtual_machine import VirtualMachine


def test_init_registers():
    num_regs = 8
    vm = VirtualMachine(num_regs=num_regs)
    assert len(vm.registers) == num_regs


def test_registers_are_registers():
    num_regs = 8
    vm = VirtualMachine(num_regs=num_regs)
    print(type(vm.registers[0]))
    for register in vm.registers:
        assert isinstance(register, Register)


def test_init_stack():
    vm = VirtualMachine(num_regs=8)
    assert isinstance(vm.stack, Stack)


def test_init_memory():
    vm = VirtualMachine(num_regs=8)
    assert isinstance(vm.memory, Memory)
