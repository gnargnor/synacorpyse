from abc import abstractmethod, ABCMeta

from synacorpyse.constants import Action
from synacorpyse.message import Message
from synacorpyse.register import Register

condition = lambda current_address : 317 < current_address < 1093
conditional_logs = True
justin_logs = False
justwrite_logs = False
justjump_logs = True
justout_logs = True
op_code_logs = False
print_letters_written_to_memory = False


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
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class Set(Operation):
    """1: Set register <a> to the value of <b>."""
    op_id = 1
    num_args = 2

    def __init__(self, a, b):
        if op_code_logs:
            print('#set')
            print(f'==> a: {a}')
            print(f'==> b: {b}')
        self.address = a.address
        self.token = b

    def operate(self, current_address, callback):
        message = Message(
            action=Action.update_register,
            args=[self.address, self.token.value]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class Push(Operation):
    """2: Push <a> onto the stack."""
    op_id = 2
    num_args = 1

    def __init__(self, a):
        self.token_value = a.value
        if op_code_logs:
            print(f'#push op')
            print(f'==> address: {a.value}')

    def operate(self, current_address, callback):
        message = Message(
            action=Action.push_stack,
            args=[self.token_value]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class Pop(Operation):
    """3: Remove the top element from the stack and write it into <a>; empty stack = error."""
    op_id = 3
    num_args = 1

    def __init__(self, a):
        self.address = a.address
        if op_code_logs:
            print(f'#pop op')
            print(f'==> address: {a}')

    def operate(self, current_address, callback):
        message = Message(
            action=Action.pop_stack,
            args=[self.address]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class Equal(Operation):
    """4: Set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise."""
    op_id = 4
    num_args = 3

    def __init__(self, a, b, c):
        self.address = a.address
        self.left = b
        self.right = c
        if op_code_logs:
            print(f'#equal op')
            print(f'==> reg num: {self.address}')
            print(f'==> b: {b}')
            print(f'==> c: {c}')

    def operate(self, current_address, callback):
        new_value = 1 if self.left.value == self.right.value else 0
        message = Message(
            action=Action.update_register,
            args=[self.address, new_value]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class GreaterThan(Operation):
    """5: Set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise."""
    op_id = 5
    num_args = 3

    def __init__(self, a, b, c):
        self.address = a.address
        self.left = b
        self.right = c
        if op_code_logs:
            print(f'#greater than op: ')
            print(f'==> reg num: {self.address}')
            print(f'==> b: {b}')
            print(f'==> c: {c}')

    def operate(self, current_address, callback):
        new_value = 1 if self.left.value > self.right.value else 0
        message = Message(
            action=Action.update_register,
            args=[self.address, new_value]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class Jump(Operation):
    """6: Jump to <a>."""
    op_id = 6
    num_args = 1

    def __init__(self, a):
        self.destination = a.value
        if op_code_logs:
            print('#jump op')
            print(f'==> destination: {self.destination}')


    def operate(self, current_address, callback):
        message = Message(
            action=Action.jump,
            args=[self.destination]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class JumpTrue(Operation):
    """7: If <a> is nonzero, jump to <b>."""
    op_id = 7
    num_args = 2

    def __init__(self, a, b):
        self.condition = a
        self.destination = b
        if op_code_logs or justjump_logs:
            print('#jump true op')
            print(f'==> condition: {self.condition}')
            print(f'==> destination: {self.destination}')

    def operate(self, current_address, callback):
        if self.condition.value != 0:
            message = Message(
                action=Action.jump,
                args=[self.destination.value]
            )
        else:
            message = Message(
                action=Action.no_op,
                args=[]
            )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class JumpFalse(Operation):
    """8: If <a> is zero, jump to <b>."""
    op_id = 8
    num_args = 2

    def __init__(self, a, b):
        self.condition = a
        self.destination = b
        if op_code_logs or justjump_logs:
            print(f'#jump false op')
            print(f'==> condition: {self.condition}')
            print(f'==> destination: {self.destination}')

    def operate(self, current_address, callback):
        if self.condition.value == 0:
            message = Message(
                action=Action.jump,
                args=[self.destination.value]
            )
        else:
            message = Message(
                action=Action.no_op,
                args=[]
            )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class Add(Operation):
    """9: Assign into <a> the sum of <b> and <c> (modulo 32768)."""
    op_id = 9
    num_args = 3

    def __init__(self, a, b, c):
        self.address = a.address
        self.left = b
        self.right = c
        if op_code_logs:
            print('#add op')
            print(f'==> address: {self.address}')
            print(f'==> left: {b}')
            print(f'==> right: {c}')

    def operate(self, current_address, callback):
        new_value = (self.left.value + self.right.value) % 32768
        message = Message(
            action=Action.update_register,
            args=[self.address, new_value]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class Multiply(Operation):
    """10: Store into <a> the product of <b> and <c> (modulo 32768)."""
    op_id = 10
    num_args = 3

    def __init__(self, a, b, c):
        self.address = a.address
        self.left = b
        self.right = c
        if op_code_logs:
            print('#mult op')
            print(f'==> address: {self.address}')
            print(f'==> left: {b}')
            print(f'==> right: {c}')

    def operate(self, current_address, callback):
        new_value = (self.left.value * self.right.value) % 32768
        message = Message(
            action=Action.update_register,
            args=[self.address, new_value]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class Modulo(Operation):
    """11: Store into <a> the remainder of <b> divided by <c>."""
    op_id = 11
    num_args = 3

    def __init__(self, a, b, c):
        self.address = a.address
        self.left = b
        self.right = c
        if op_code_logs:
            print('#mod op')
            print(f'==> address: {self.address}')
            print(f'==> left: {b}')
            print(f'==> right: {c}')

    def operate(self, current_address, callback):
        new_value = self.left.value % self.right.value
        message = Message(
            action=Action.update_register,
            args=[self.address, new_value]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class And(Operation):
    """12: Stores into <a> the bitwise and of <b> and <c>."""
    op_id = 12
    num_args = 3

    def __init__(self, a, b, c):
        self.address = a.address
        self.left = b
        self.right = c
        if op_code_logs:
            print('#and op')
            print(f'==> address: {self.address}')
            print(f'==> left: {b}')
            print(f'==> right: {c}')

    def operate(self, current_address, callback):
        new_value = (self.left.value & self.right.value)
        message = Message(
            action=Action.update_register,
            args=[self.address, new_value]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class Or(Operation):
    """13: Stores into <a> the bitwise or of <b> and <c>."""
    op_id = 13
    num_args = 3

    def __init__(self, a, b, c):
        self.address = a.address
        self.left = b
        self.right = c
        if op_code_logs:
            print('#or op')
            print(f'==> address: {self.address}')
            print(f'==> left: {b}')
            print(f'==> right: {c}')

    def operate(self, current_address, callback):
        new_value = (self.left.value | self.right.value)
        message = Message(
            action=Action.update_register,
            args=[self.address, new_value]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class Not(Operation):
    """14: Stores 15-bit bitwise inverse of <b> in <a>."""
    op_id = 14
    num_args = 2

    def __init__(self, a, b):
        self.address = a.address
        self.original = b
        if op_code_logs:
            print('#not op')
            print(f'==> address: {self.address}')
            print(f'==> orig: {b}')

    def operate(self, current_address, callback):
        def bit_not(n, numbits=15):
            return (1 << numbits) - 1 - n

        new_value = bit_not(self.original.value)
        message = Message(
            action=Action.update_register,
            args=[self.address, new_value]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class ReadMemory(Operation):
    """15: Read memory at address <b> and write it to <a>."""
    op_id = 15
    num_args = 2

    def __init__(self, a, b):
        self.target_address = a.address
        self.memory_address = b.value
        if op_code_logs:
            print('#read memory opcode')
            print(f'==> address: {self.target_address}')
            print(f'==> mem address: {self.memory_address}')

    def operate(self, current_address, callback):
        message = Message(
            action=Action.read_memory,
            args=[self.target_address, self.memory_address]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class WriteMemory(Operation):
    """16: Write the value from <b> into memory at address <a>."""
    op_id = 16
    num_args = 2

    def __init__(self, a, b):
        if print_letters_written_to_memory:
            print(chr(b.value), end='')
        self.target_address = a.value
        self.source_token = b.value
        if op_code_logs or justwrite_logs:
            print('#write memory op')
            print(f'==> target_address: {a.value}')
            print(f'==> source token: {b.value}')
        # self.memory_address = a
        # self.register: Register = b

    def operate(self, current_address, callback):
        message = Message(
            action=Action.write_memory,
            args=[self.target_address, self.source_token]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)
        # memory[memory_address].value = self.storage_location.value


class Call(Operation):
    """17: Write the address of the next instruction to the stack and jump to <a>."""
    op_id = 17
    num_args = 1

    def __init__(self, a):
        self.destination = a.value
        if op_code_logs:
            print(f'#call op')
            print(f'==> destination: {a}')

    def operate(self, current_address, callback):
        message = Message(
            action=Action.call,
            args=[current_address, self.destination]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class Return(Operation):
    """18: Remove the top element from the stack and jump to it; empty stack = halt."""
    op_id = 18
    num_args = 0

    def __init__(self):
        if op_code_logs:
            print('#return op')

    def operate(self, current_address, callback):
        message = Message(
            action=Action.ret,
            args=[]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class Out(Operation):
    """19: write the character represented by ascii code <a> to the terminal."""
    op_id = 19
    num_args = 1

    def __init__(self, a):
        self.ascii_code = a
        if op_code_logs or justout_logs:
            print('#out op')
            print(f'==> ascii code: {chr(a.value)}')

    def operate(self, current_address, callback):
        print(f'current address: {current_address}')
        message = Message(
            action=Action.update_display,
            args=[self.ascii_code]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
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
        self.write_location = a
        if op_code_logs or justin_logs:
            print(f'#in op')
            print(f'==> write location: {a}')

    def operate(self, current_address, callback):
        user_input = input('type stuff: ')
        self.write_location.value = user_input
        message = Message(
            action=Action.update_register,
            args=[self.write_location]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


class NoOp(Operation):
    """21: No operation."""
    op_id = 21
    num_args = 0

    def __init__(self):
        if op_code_logs:
            print('#no op')

    def operate(self, current_address, callback):
        message = Message(
            action=Action.no_op,
            args=[]
        )
        if conditional_logs and condition(current_address):
            print('**')
            print(f'current address: {current_address}')
            print(message.action)
            print(message.args)
            print('**')
            print()
        return callback(message)


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
