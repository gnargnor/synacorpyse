memory_super_logs = False

class Memory:
    @property
    def tokens(self):  # Are tokens the same as the memory?
                       # Are tokens the abstract syntax tree
                       # created by reading the program?
        return self.__tokens

    @property
    def position(self):
        return self.__position

    def __init__(self, tokens, position=0):
        self.__tokens = tokens
        self.__position = position

    def set_next(self, next=None):
        if next is None:
            self.__position += 1
        else:
            self.__position = next

    def current_token(self):
        return self.__tokens[self.__position]

    def write(self, location, token):
        if memory_super_logs:
            print(f'token at location {location}: {self.__tokens[location]}')
        self.__tokens[location].value = token

    def read(self, location):
        if memory_super_logs:
            print(f'read memory in memory class: {self.__tokens[location]}')
        return self.__tokens[location].value
