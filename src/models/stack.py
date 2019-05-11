from typing import List

from models.value import Value


class EmptyStackError(Exception):
    def __init__(self):
        message = 'Pop called on empty stack.'
        super().__init__(message)


class Stack:
    @property
    def stack(self):
        return self.__stack

    def __init__(self):
        self.__stack: List[Value] = []

    def __len__(self):
        return len(self.stack)

    def push(self, value: Value) -> None:
        self.stack.append(value)

    def pop(self) -> Value:
        if not len(self.stack):
            raise EmptyStackError
        return self.stack.pop()
