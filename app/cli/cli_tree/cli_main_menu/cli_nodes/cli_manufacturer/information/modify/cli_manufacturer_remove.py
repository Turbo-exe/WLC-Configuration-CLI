from rich.console import Console
from rich.panel import Panel

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.cli_components.yes_no import YesNo
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.inventory.dao.dao_manufacturer import DaoManufacturer
from app.inventory.model.manufacturer import Manufacturer


class MenuManufacturerRemove(Menu):
    def __init__(self, console: Console, manufacturer: Manufacturer):
        super().__init__(
            console=console,
            path=CLIPaths.MANUFACTURER_REMOVE.value
        )
        self.manufacturer = manufacturer

    def start(self):
        if YesNo(console=self.console,
                 prompt="Are you sure? All hosts and groups of that manufacturer "
                        "type will be deleted as well!"
                        "This cannot be undone!").decision:

            DaoManufacturer().delete_manufacturer(
                manufacturer=self.manufacturer
            )
            self.console.print(
                Panel(f"The manufacturer {self.manufacturer.name} has been deleted successfully!",
                      title="Process completed!"),
                style=str(Color.SUCCESS.value)
            )
        else:
            self.console.print(
                Panel(f"The process has been aborted!",
                      title="Process aborted!"),
                style=str(Color.FAIL.value)
            )
        wait_for_user_to_continue(console=self.console)
