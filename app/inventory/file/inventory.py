from app.inventory.file.write_inventory import WriteInventory
from contextlib import contextmanager


class Inventory(WriteInventory):
    @contextmanager
    def readwrite(self, send: bool = True) -> None:
        try:
            self.read_inventory()
            yield self
            self.write_inventory()
            if send:
                print("Sending to raspberry pi...")
        except (Exception, SystemExit) as exception:
            raise self.InventoryCriticalError(exception)

    @contextmanager
    def read(self) -> None:
        try:
            self.read_inventory()
            yield self
        except (Exception, SystemExit) as exception:
            raise self.InventoryCriticalError(exception)

    class InventoryCriticalError(Exception):
        def __init__(self, exception):
            raise exception
