from dataclasses import dataclass

from typing import List, Any

from synacorpyse.constants import Action


class InvalidActionError(Exception):
    def __init__(self, message):
        super().__init__(message)


@dataclass
class Message:
    action: Action
    args: List[Any]

    def __post_init__(self):
        if not isinstance(self.action, Action):
            raise InvalidActionError(f'{self.action}')
