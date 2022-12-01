from rich.console import Console
from rich.panel import Panel

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.inventory.dao.dao_manufacturer import DaoManufacturer
from app.inventory.model.manufacturer import Manufacturer


class MenuManufacturerRename(Menu):
    def __init__(self, console: Console, manufacturer: Manufacturer):
        super().__init__(
            console=console,
            path=CLIPaths.MANUFACTURER_RENAME.value
        )
        self.manufacturer = manufacturer

    def start(self):
        new_name = input(f"\nPlease enter the new name for the manufacturer \"{self.manufacturer.name}\": ").upper()
        try:
            DaoManufacturer().rename_manufacturer(
                manufacturer=self.manufacturer,
                new_name=new_name
            )
        except Manufacturer.ManufacturerNameInvalidException:
            self.console.print(
                Panel("This name is invalid. It must not contain '___' or a number on the start!",
                      title="Process aborted!"),
                style=str(Color.FAIL.value))
        except Manufacturer.ManufacturerExistsException:
            self.console.print(
                Panel("This manufacturer name is already in use! The process will be aborted.",
                      title="Process aborted!"),
                style=str(Color.FAIL.value))
        else:
            self.console.print(
                Panel(f"The manufacturer {self.manufacturer.name} has been renamed successfully to {new_name}!",
                      title="Process completed!"),
                style=str(Color.SUCCESS.value)
            )
        wait_for_user_to_continue(console=self.console)
