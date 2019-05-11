from models import opcode


class InvalidCommandValueError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Token:
    def __init__(self, type: str, value: int, address: int):
        print(f'type: {type}')
        print(f'value: {value}')
        print(f'------------------')
        self.type = type
        self.value = value
        self.address = address


class Command(Token):
    def __init__(self, value: int, address: int):
        if 21 < value:
            raise InvalidCommandValueError(f'Unknown token type.')
        super().__init__('COMMAND', value, address)
        self.operation = self.get_operation()

    def get_operation(self):
        return opcode.opcode_map[self.value]

    def get_num_args(self) -> int:
        return self.operation.__code__.co_argcount

    @staticmethod
    def is_valid():
        return True


class Argument(Token):
    def __init__(self, value: int, address: int, arg_num):
        super().__init__('ARGUMENT', value, address)
        self.arg_num = arg_num

    @staticmethod
    def is_valid():
        return True


class Unknown(Token):
    def __init__(self, value: int, address: int):
        super().__init__('UNKNOWN', value, address)

    @staticmethod
    def is_valid():
        return False


def Tokens(input_values):
    limit = len(input_values)
    address = 0
    arguments = []

    while address < limit:
        print(f'address: {address}')
        print(f'arguments: {arguments}')

        if not len(arguments):
            try:
                token = Command(input_values[address], address)
                num_args = token.get_num_args()
                arguments = list(reversed(range(num_args)))
            except InvalidCommandValueError as ex:
                print(ex)
                token = Unknown(input_values[address], address)
            yield token
        else:
            token = Argument(input_values[address], address, arguments.pop())
            yield token

        address += 1
