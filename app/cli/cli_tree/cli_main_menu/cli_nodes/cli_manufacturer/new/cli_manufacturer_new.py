from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.enum.cli_options import CLIPaths
from rich.panel import Panel

from app.cli.enum.color import Color
from app.inventory.dao.dao_manufacturer import DaoManufacturer
from app.inventory.model.manufacturer import Manufacturer


class MenuManufacturerNew(Menu):
    def __init__(self, console):
        super().__init__(
            console=console,
            path=CLIPaths.MANUFACTURER_NEW.value
        )

    def start(self):
        name = input("\nPlease enter the name of the new manufacturer: ").upper()
        try:
            DaoManufacturer().add_manufacturer(
                manufacturer_name=name
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
                Panel(f"The manufacturer {name} has been added successfully!",
                      title="Process completed!"),
                style=str(Color.SUCCESS.value)
            )
        wait_for_user_to_continue(console=self.console)
