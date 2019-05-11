from abc import abstractmethod, ABCMeta
import sys


from models.register import Register
from models.stack import Stack


class Operation(metaclass=ABCMeta):
    @property
    @abstractmethod
    def num_args(self):
        pass

    @abstractmethod
    def operate(self):
        pass


class Halt(Operation):
    """0: Stop execution and terminate the program. """
    num_args = 0

    def operate(self):
        sys.exit()


class Set(Operation):
    """1: Set register <a> to the value of <b>."""
    num_args = 2

    def __init__(self, a, b):
        self.register: Register = a
        self.value: int = b

    def operate(self):
        self.register.set_value(self.value)


class Push(Operation):
    """2: Push <a> onto the stack."""
    num_args = 1

    def __init__(self, a):
        self.value = a

    def operate(self):
        pass


class Pop(Operation):
    """3: Remove the top element from the stack and write it into <a>; empty stack = error."""
    num_args = 1

    def __init__(self, a):
        self.destination = a

    def operate(self):
        pass


def pop_op(a):
    """
    3: Remove the top element from the stack and write it into <a>; empty stack = error.
    :param a:
    :return:
    """
    pass


def eq_op(a, b, c):
    """
    4: Set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise.
    :param a:
    :param b:
    :param c:
    :return:
    """
    pass


def gt_op(a, b, c):
    """
    5: Set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise.
    :param a:
    :param b:
    :param c:
    :return:
    """
    pass


def jmp_op(a):
    """
    6: Jump to <a>.
    :param a:
    :return:
    """
    pass


def jt_op(a, b):
    """
    7: If <a> is nonzero, jump to <b>.
    :param a:
    :param b:
    :return:
    """
    pass


def jf_op(a, b):
    """
    8: If <a> is zero, jump to <b>.
    :param a:
    :param b:
    :return:
    """
    pass


def add_op(a, b, c):
    """
    9: Assign into <a> the sum of <b> and <c> (modulo 32768).
    :param a:
    :param b:
    :param c:
    :return:
    """
    pass


def mult_op(a, b, c):
    """
    10: Store into <a> the product of <b> and <c> (modulo 32768).
    :param a:
    :param b:
    :param c:
    :return:
    """
    pass


def mod_op(a, b, c):
    """
    11: Store into <a> the remainder of <b> divided by <c>.
    :param a:
    :param b:
    :param c:
    :return:
    """
    pass


def and_op(a, b, c):
    """
    12: Stores into <a> the bitwise and of <b> and <c>.
    :param a:
    :param b:
    :param c:
    :return:
    """
    pass


def or_op(a, b, c):
    """
    13: Stores into <a> the bitwise or of <b> and <c>.
    :param a:
    :param b:
    :param c:
    :return:
    """
    pass


def not_op(a, b):
    """
    14: Stores 15-bit bitwise inverse of <b> in <a>.
    :param a:
    :param b:
    :return:
    """
    pass


def rmem_op(a, b):
    """
    15: Read memory at address <b> and write it to <a>.
    :param a:
    :param b:
    :return:
    """
    pass


def wmem_op(a, b):
    """
    16: Write the value from <b> into memory at address <a>.
    :param a:
    :param b:
    :return:
    """
    pass


def call_op(a):
    """
    17: Write the address of the next instruction to the stack and jump to <a>.
    :param a:
    :return:
    """
    pass


def ret_op():
    """
    18: Remove the top element from the stack and jump to it; empty stack = halt.
    :return:
    """
    pass


def out_op(a):
    """
    19: write the character represented by ascii code <a> to the terminal.
    :param a:
    :return:
    """
    pass


def in_op(a):
    """
    20: Read a character from the terminal and write its ascii code to <a>;
    it can be assumed that once input starts, it will continue until a newline is encountered;
    this means that you can safely read whole lines from the keyboard and trust that they will be fully read.
    :param a:
    :return:
    """
    pass


def noop_op():
    """
    21: no operation
    :return:
    """
    pass


opcode_map = {
    0: halt_op,
    1: set_op,
    2: push_op,
    3: pop_op,
    4: eq_op,
    5: gt_op,
    6: jmp_op,
    7: jt_op,
    8: jf_op,
    9: add_op,
    10: mult_op,
    11: mod_op,
    12: and_op,
    13: or_op,
    14: not_op,
    15: rmem_op,
    16: wmem_op,
    17: call_op,
    18: ret_op,
    19: out_op,
    20: in_op,
    21: noop_op
}


def operation(code):
    return opcode_map[code]





