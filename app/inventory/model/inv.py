from dataclasses import dataclass

from app.inventory.model.manufacturer import Manufacturer


@dataclass
class Inv:
    manufacturers: list[Manufacturer] = None
