from abc import abstractmethod, ABCMeta
import sys


from models.memory import Memory
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

    def get_storage(self, location):
        """When an operation is given a storage reference, we need a way to fetch that object and update it."""
        pass


class Halt(Operation):
    """0: Stop execution and terminate the program. """
    op_id = 0
    num_args = 0

    def operate(self):
        sys.exit()

    def repr(self):
        return f'{self.__class__.__name__}(' \
            f'{self.op_id}: num_args: {self.num_args}'


class Set(Operation):
    """1: Set register <a> to the value of <b>."""
    num_args = 2

    def __init__(self, a, b):
        self.register: Register = a
        self.value: int = b

    def operate(self):
        self.register.value(self.value)


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


class Equal(Operation):
    """4: Set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise."""
    num_args = 3

    def __init__(self, a, b, c):
        self.storage_location = a
        self.left = b
        self.right = c

    def operate(self):
        self.storage_location = 1 if self.left == self.right else 0


class GreaterThan(Operation):
    """5: Set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise."""
    num_args = 3

    def __init(self, a, b, c):
        self.storage_location = a
        self.left = b
        self.right = c

    def operate(self):
        self.storage_location.value = 1 if self.left > self.right else 0


class Jump(Operation):
    """6: Jump to <a>."""
    num_args = 1

    def __init__(self, a):
        self.destination = a

    def operate(self):
        return self.destination.value


class JumpTrue(Operation):
    """7: If <a> is nonzero, jump to <b>."""
    num_args = 2

    def __init__(self, a, b):
        self.condition = a
        self.destination = b

    def operate(self):
        if self.condition.value != 0:
            return self.destination.value


class JumpFalse(Operation):
    """8: If <a> is zero, jump to <b>."""
    num_args = 2

    def __init__(self, a, b):
        self.condition = a
        self.destination = b

    def operate(self):
        if self.condition.value == 0:
            return self.destination.value


class Add(Operation):
    """9: Assign into <a> the sum of <b> and <c> (modulo 32768)."""
    num_args = 3

    def __init__(self, a, b, c):
        self.storage_location = a
        self.left = b
        self.right = c

    def operate(self):
        self.storage_location.value = (self.left + self.right) % 32768


class Multiply(Operation):
    """10: Store into <a> the product of <b> and <c> (modulo 32768)."""
    num_args = 3

    def __init__(self, a, b, c):
        self.storage_location = a
        self.left = b
        self.right = c

    def operate(self):
        self.storage_location.value = (self.left * self.right) % 32768


class Modulo(Operation):
    """11: Store into <a> the remainder of <b> divided by <c>."""
    num_args = 3

    def __init__(self, a, b, c):
        self.storage_location = a
        self.left = b
        self.right = c

    def operate(self):
        self.storage_location.value = self.left % self.right


class And(Operation):
    """12: Stores into <a> the bitwise and of <b> and <c>."""
    num_args = 3

    def __init__(self, a, b, c):
        self.storage_location = a
        self.left = b
        self.right = c

    def operate(self):
        pass


class Or(Operation):
    """13: Stores into <a> the bitwise or of <b> and <c>."""
    num_args = 3

    def __init__(self, a, b, c):
        self.storage_location = a
        self.left = b
        self.right = c

    def operate(self):
        pass


class Not(Operation):
    """14: Stores 15-bit bitwise inverse of <b> in <a>."""
    num_args = 2

    def __init__(self, a, b):
        self.storage_location = a
        self.original = b

    def operate(self):
        pass


class ReadMemory(Operation):
    """15: Read memory at address <b> and write it to <a>."""
    num_args = 2

    def __init__(self, a ,b):
        self.storage_location = a
        self.memory_address = b

    def operate(self):
        pass
        # self.storage_location.value = memory[self.memory_address]


class WriteMemory(Operation):
    """16: Write the value from <b> into memory at address <a>."""
    num_args = 2

    def __init__(self, a, b):
        self.memory_address = a
        self.storage_location = b

    def operate(self):
        pass
        # memory[memory_address].value = self.storage_location.value


class Call(Operation):
    """17: Write the address of the next instruction to the stack and jump to <a>."""
    num_args = 1

    def __init__(self, a):
        self.destination = a

    def operate(self):
        pass


class Return(Operation):
    """18: Remove the top element from the stack and jump to it; empty stack = halt."""
    num_args = 0

    def __init__(self):
        pass

    def operate(self):
        pass


class Out(Operation):
    """19: write the character represented by ascii code <a> to the terminal."""
    num_args = 1

    def __init__(self, a):
        self.character_token = a

    def operate(self):
        return chr(self.character_token.value)


class In(Operation):
    """
    20: Read a character from the terminal and write its ascii code to <a>;
    it can be assumed that once input starts, it will continue until a newline is encountered;
    this means that you can safely read whole lines from the keyboard and trust that they will be fully read.
    """
    num_args = 1

    def __init__(self, a):
        pass

    def operate(self):
        pass


class NoOp(Operation):
    """21: No operation."""
    num_args = 0

    def __init__(self):
        pass

    def operate(self):
        pass


opcode_map = {
    0: Halt,
    1: Set,
    2: Push,
    3: Pop,
    4: Equal,
    5: GreaterThan,
    6: Jump,
    7: JumpTrue,
    8: JumpFalse,
    9: Add,
    10: Multiply,
    11: Modulo,
    12: And,
    13: Or,
    14: Not,
    15: ReadMemory,
    16: WriteMemory,
    17: Call,
    18: Return,
    19: Out,
    20: In,
    21: NoOp
}


def operation(code):
    return opcode_map[code]





