import pytest

from synacorpyse.register import Register


def test_register_address():
    register = Register(address=0)
    assert register.address == 0


def test_set_register_value():
    register = Register(address=0)
    register.value = 12345
    assert register.value == 12345


@pytest.mark.xfail(strict=True)
def test_set_register_address_fails():
    register = Register(address=0)
    register.address = 7
    assert register.address == 7
