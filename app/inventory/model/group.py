from dataclasses import dataclass
from typing import Optional

from app.cli.cli_components.user_input import UserInput


@dataclass
class Group:
    name: str
    manufacturer_name: str
    hosts: Optional[list] = None
    children: Optional[list] = None

    @staticmethod
    def validate_name(name: str) -> None:
        try:
            if name:
                int(name)
                raise Group.InvalidName("Bad name. The name must not be a number!")
        except ValueError:
            pass

    class InvalidName(Exception):
        def __init__(self, message):
            self.message = message
