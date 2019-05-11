from typing import List

from models.value import Value


class Stack:
    __stack: List[Value]

    def __init__(self):
        pass

    def push(self, value) -> None:
        self.__stack.append(value)

    def pop(self) -> Value:
        return self.__stack.pop()
