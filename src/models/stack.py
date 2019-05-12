from typing import List


class EmptyStackError(Exception):
    def __init__(self):
        message = 'Pop called on empty stack.'
        super().__init__(message)


class Stack:
    @property
    def stack(self):
        return self.__stack

    def __init__(self):
        self.__stack: List[int] = []

    def __len__(self):
        return len(self.stack)

    def push(self, value) -> None:
        self.stack.append(value)

    def pop(self):
        if not len(self.stack):
            raise EmptyStackError
        return self.stack.pop()
