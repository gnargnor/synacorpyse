from abc import abstractmethod, ABCMeta

from synacorpyse.constants import Action
from synacorpyse.message import Message
from synacorpyse.register import Register


class Operation(metaclass=ABCMeta):
    @property
    @abstractmethod
    def num_args(self):
        pass

    @property
    @abstractmethod
    def op_id(self):
        pass

    @abstractmethod
    def operate(self, current_address, callback):
        pass

    def get_storage(self, location):
        """When an operation is given a storage reference, we need a way to fetch that object and update it."""
        pass

    def repr(self):
        return f'{self.__class__.__name__}(' \
            f'{self.op_id}: num_args: {self.num_args}'


class Halt(Operation):
    """0: Stop execution and terminate the program. """
    op_id = 0
    num_args = 0

    def operate(self, current_address, callback):
        message = Message(
            action=Action.halt,
            args=[]
        )
        return callback(message)


class Set(Operation):
    """1: Set register <a> to the value of <b>."""
    op_id = 1
    num_args = 2

    def __init__(self, a, b):
        self.register: Register = a
        self.token = b

    def operate(self, current_address, callback):
        self.register.value = self.token.value
        message = Message(
            action=Action.update_register,
            args=[self.register]
        )
        return callback(message)


class Push(Operation):
    """2: Push <a> onto the stack."""
    op_id = 2
    num_args = 1

    def __init__(self, a):
        self.token = a

    def operate(self, current_address, callback):
        message = Message(
            action=Action.push_stack,
            args=[self.token]
        )
        return callback(message)


class Pop(Operation):
    """3: Remove the top element from the stack and write it into <a>; empty stack = error."""
    op_id = 3
    num_args = 1

    def __init__(self, a):
        self.register = a

    def operate(self, current_address, callback):
        message = Message(
            action=Action.pop_stack,
            args=[self.register]
        )
        return callback(message)


class Equal(Operation):
    """4: Set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise."""
    op_id = 4
    num_args = 3

    def __init__(self, a, b, c):
        self.register: Register = a
        self.left = b
        self.right = c

    def operate(self, current_address, callback):
        self.register.value = 1 if self.left.value == self.right.value else 0
        message = Message(
            action=Action.update_register,
            args=[self.register]
        )
        return callback(message)


class GreaterThan(Operation):
    """5: Set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise."""
    op_id = 5
    num_args = 3

    def __init__(self, a, b, c):
        self.register: Register = a
        self.left = b
        self.right = c

    def operate(self, current_address, callback):
        self.register.value = 1 if self.left.value > self.right.value else 0
        message = Message(
            action=Action.update_register,
            args=[self.register]
        )
        return callback(message)


class Jump(Operation):
    """6: Jump to <a>."""
    op_id = 6
    num_args = 1

    def __init__(self, a):
        self.destination = a

    def operate(self, current_address, callback):
        message = Message(
            action=Action.jump,
            args=[self.destination]
        )
        return callback(message)


class JumpTrue(Operation):
    """7: If <a> is nonzero, jump to <b>."""
    op_id = 7
    num_args = 2

    def __init__(self, a, b):
        self.condition = a
        self.destination = b

    def operate(self, current_address, callback):
        if self.condition.value != 0:
            message = Message(
                action=Action.jump,
                args=[self.destination]
            )
        else:
            message = Message(
                action=Action.no_op,
                args=[]
            )
        return callback(message)


class JumpFalse(Operation):
    """8: If <a> is zero, jump to <b>."""
    op_id = 8
    num_args = 2

    def __init__(self, a, b):
        self.condition = a
        self.destination = b

    def operate(self, current_address, callback):
        if self.condition.value == 0:
            message = Message(
                action=Action.jump,
                args=[self.destination]
            )
        else:
            message = Message(
                action=Action.no_op,
                args=[]
            )
        return callback(message)


class Add(Operation):
    """9: Assign into <a> the sum of <b> and <c> (modulo 32768)."""
    op_id = 9
    num_args = 3

    def __init__(self, a, b, c):
        self.register: Register = a
        self.left = b
        self.right = c

    def operate(self, current_address, callback):
        self.register.value = (self.left.value + self.right.value) % 32768
        message = Message(
            action=Action.update_register,
            args=[self.register]
        )
        return callback(message)


class Multiply(Operation):
    """10: Store into <a> the product of <b> and <c> (modulo 32768)."""
    op_id = 10
    num_args = 3

    def __init__(self, a, b, c):
        self.register: Register = a
        self.left = b
        self.right = c

    def operate(self, current_address, callback):
        self.register.value = (self.left.value * self.right.value) % 32768
        message = Message(
            action=Action.update_register,
            args=[self.register]
        )
        return callback(message)


class Modulo(Operation):
    """11: Store into <a> the remainder of <b> divided by <c>."""
    op_id = 11
    num_args = 3

    def __init__(self, a, b, c):
        self.register: Register = a
        self.left = b
        self.right = c

    def operate(self, current_address, callback):
        self.register.value = self.left.value % self.right.value
        message = Message(
            action=Action.update_register,
            args=[self.register]
        )
        return callback(message)


class And(Operation):
    """12: Stores into <a> the bitwise and of <b> and <c>."""
    op_id = 12
    num_args = 3

    def __init__(self, a, b, c):
        self.register: Register = a
        self.left = b
        self.right = c

    def operate(self, current_address, callback):
        self.register.value = (self.left.value & self.right.value)
        message = Message(
            action=Action.update_register,
            args=[self.register]
        )
        return callback(message)


class Or(Operation):
    """13: Stores into <a> the bitwise or of <b> and <c>."""
    op_id = 13
    num_args = 3

    def __init__(self, a, b, c):
        self.register: Register = a
        self.left = b
        self.right = c

    def operate(self, current_address, callback):
        self.register.value = (self.left.value | self.right.value)
        message = Message(
            action=Action.update_register,
            args=[self.register]
        )
        return callback(message)


class Not(Operation):
    """14: Stores 15-bit bitwise inverse of <b> in <a>."""
    op_id = 14
    num_args = 2

    def __init__(self, a, b):
        self.register: Register = a
        self.original = b

    def operate(self, current_address, callback):
        def bit_not(n, numbits=15):
            return (1 << numbits) - 1 - n

        self.register.value = bit_not(self.original.value)
        message = Message(
            action=Action.update_register,
            args=[self.register]
        )
        return callback(message)


class ReadMemory(Operation):
    """15: Read memory at address <b> and write it to <a>."""
    op_id = 15
    num_args = 2

    def __init__(self, a, b):
        self.register: Register = a
        self.memory_address = b

    def operate(self, current_address, callback):
        message = Message(
            action=Action.read_memory,
            args=[self.register, self.memory_address]
        )
        return callback(message)
        # self.storage_location.value = memory[self.memory_address]


class WriteMemory(Operation):
    """16: Write the value from <b> into memory at address <a>."""
    op_id = 16
    num_args = 2

    def __init__(self, a, b):
        # print('88888888888888888888888888888888888888888888888')
        # print(a)
        print(chr(b.value), end='')
        self.target = a
        self.source = b
        # self.memory_address = a
        # self.register: Register = b

    def operate(self, current_address, callback):
        message = Message(
            action=Action.write_memory,
            args=[self.target, self.source]
        )
        return callback(message)
        # memory[memory_address].value = self.storage_location.value


class Call(Operation):
    """17: Write the address of the next instruction to the stack and jump to <a>."""
    op_id = 17
    num_args = 1

    def __init__(self, a):
        self.destination = a

    def operate(self, current_address, callback):
        message = Message(
            action=Action.call,
            args=[current_address, self.destination]
        )
        return callback(message)


class Return(Operation):
    """18: Remove the top element from the stack and jump to it; empty stack = halt."""
    op_id = 18
    num_args = 0

    def __init__(self):
        pass

    def operate(self, current_address, callback):
        message = Message(
            action=Action.ret,
            args=[]
        )
        return callback(message)


class Out(Operation):
    """19: write the character represented by ascii code <a> to the terminal."""
    op_id = 19
    num_args = 1

    def __init__(self, a):
        self.ascii_code = a

    def operate(self, current_address, callback):
        message = Message(
            action=Action.update_display,
            args=[self.ascii_code]
        )
        return callback(message)


class In(Operation):
    """
    20: Read a character from the terminal and write its ascii code to <a>;
    it can be assumed that once input starts, it will continue until a newline is encountered;
    this means that you can safely read whole lines from the keyboard and trust that they will be fully read.
    """
    op_id = 20
    num_args = 1

    def __init__(self, a):
        print(type(a))
        self.write_location = a
        pass

    def operate(self, current_address, callback):
        user_input = input('type stuff: ')
        self.write_location.value = user_input
        message = Message(
            action=Action.update_register,
            args=[self.write_location]
        )
        return callback(message)


class NoOp(Operation):
    """21: No operation."""
    op_id = 21
    num_args = 0

    def __init__(self):
        pass

    def operate(self, current_address, callback):
        message = Message(
            action=Action.no_op,
            args=[]
        )
        return callback(message)
        # pass


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
