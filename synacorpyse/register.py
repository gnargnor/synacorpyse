class Register:
    @property
    def reg_num(self):
        return self.__reg_num

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __init__(self, reg_num):
        self.__reg_num = reg_num
        self.value = 0

    def __repr__(self):
        return f'{self.__class__.__name__} (' \
            f'value={self.value})'
