from dataclasses import dataclass
from typing import Optional

from app.inventory.model.group import Group


@dataclass
class Manufacturer:
    name: str
    hosts: Optional[list] = None
    children: Optional[list[Group]] = None

    @staticmethod
    def validate_name(name: str) -> bool:
        if len(name) == 0:
            return True
        if name.find(":") != -1:
            return True
        try:
            int(name[0])
            return True
        except ValueError:
            pass
        return False

    class ManufacturerExistsException(Exception):
        pass

    class ManufacturerNameInvalidException(Exception):
        pass
