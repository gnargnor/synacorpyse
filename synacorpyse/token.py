from synacorpyse import opcode


class InvalidCommandValueError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Token:
    def __init__(self, type: str, value: int, address: int):
        self.type = type
        self.value = value
        self.address = address


class Command(Token):
    def __init__(self, value: int, address: int):
        if 21 < value:
            raise InvalidCommandValueError(f'Unknown token type.')
        super().__init__('COMMAND', value, address)
        self.operation = self.get_operation()

    def __repr__(self):
        return f'{self.__class__.__name__} (' \
            f'value={self.value}, address={self.address}, operation={self.operation})'

    def get_operation(self):
        return opcode.opcode_map[self.value]

    def get_num_args(self) -> int:
        return self.operation.num_args

    @staticmethod
    def is_valid():
        return True


class Argument(Token):
    def __init__(self, value: int, address: int = None, arg_num=None):
        super().__init__('ARGUMENT', value, address)
        self.arg_num = arg_num

    def __repr__(self):
        return f'{self.__class__.__name__} (' \
            f'value={self.value}, address={self.address}, arg_num={self.arg_num})'

    @staticmethod
    def is_valid():
        return True


class Unknown(Token):
    def __init__(self, value: int, address: int):
        super().__init__('UNKNOWN', value, address)

    def __repr__(self):
        return f'{self.__class__.__name__} (' \
            f'value={self.value}, address={self.address})'

    @staticmethod
    def is_valid():
        return False


def Tokens(input_values):
    limit = len(input_values)
    address = 0
    arguments = []

    while address < limit:
        if not len(arguments):
            try:
                token = Command(input_values[address], address)
                num_args = token.get_num_args()
                arguments = list(reversed(range(num_args)))
            except InvalidCommandValueError as ex:
                token = Unknown(input_values[address], address)
            yield token
        else:
            token = Argument(input_values[address], address, arguments.pop())
            yield token

        address += 1
