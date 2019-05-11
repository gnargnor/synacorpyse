from models.value import Value


class Register:
    @property
    def address(self):
        return self.__address

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: Value):
        self.__value = value

    def __init__(self, address):
        self.__address = address
