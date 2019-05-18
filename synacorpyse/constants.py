from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Action(AutoName):
    update_register = auto()
    read_memory = auto()
    write_memory = auto()
    update_display = auto()
    push_stack = auto()
    pop_stack = auto()
    jump = auto()
    halt = auto()
    call = auto()
    ret = auto()
    no_op = auto()
