import pytest

from stack import Stack, EmptyStackError


def test_push_stack():
    stack = Stack()
    value = 12345
    stack.push(value)
    assert len(stack) == 1


def test_pop_stack():
    stack = Stack()
    value = 12345
    stack.push(value)
    assert len(stack) == 1
    popped_value = stack.pop()
    assert popped_value == value
    assert len(stack) == 0


def test_empty_stack_throws_error_on_pop():
    stack = Stack()
    with pytest.raises(EmptyStackError):
        error_expected = stack.pop()
