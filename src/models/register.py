class Register:
    @property
    def address(self):
        return self.__address

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __init__(self, address):
        self.__address = address
        self.value = 0

    def __repr__(self):
        return f'{self.__class__.__name__} (' \
            f'value={self.value}, address={self.address})'
