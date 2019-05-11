class Register:
    __address = None
    __value = None

    def __init__(self, address):
        self.__address = address

    def set_value(self, value):
        self.__value = value
