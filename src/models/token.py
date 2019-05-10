from models import opcode


class Token:
    def __init__(self, type: str, value: int, address: int):
        print(f'value: {value}')
        print(f'------------------')
        self.type = type
        self.value = value
        self.address = address


class Command(Token):
    def __init__(self, value: int, address: int):
        print('COMMAND')
        super().__init__('COMMAND', value, address)
        self.operation = self.get_command()

    def get_command(self):
        return opcode.opcode_map[self.value]

    def get_num_args(self) -> int:
        return self.operation.__code__.co_argcount


class Argument(Token):
    def __init__(self, value: int, address: int, arg_num):
        print('ARGUMENT')
        super().__init__('ARGUMENT', value, address)
        self.arg_num = arg_num


# class Number(Argument):
#     def __init__(self, value, address):
#         super().__init__('NUMBER', value, address)
#
#
# class Register(Argument):
#     """Numbers 32768..32775 instead mean registers 0..7"""
#     def __init__(self, value, address):
#         value = value - 32768
#         super().__init__('REGISTER', value, address)
#
#
# class Character(Argument):
#     pass


def Tokens(input_values):
    end = len(input_values) + 1
    address = 0
    arguments = []

    while address < end:
        print(f'address: {address}')
        # print(f'command: {command}')
        print(f'arguments: {arguments}')

        if not len(arguments):
            token = Command(input_values[address], address)
            num_args = token.get_num_args()
            arguments = list(reversed(range(num_args)))
            yield token
        else:
            token = Argument(input_values[address], address, arguments.pop())
            yield token

        address += 1
