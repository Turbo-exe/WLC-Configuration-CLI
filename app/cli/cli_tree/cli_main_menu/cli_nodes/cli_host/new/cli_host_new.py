from rich.panel import Panel

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_host.cli_host_inputs import CLIHostInputs
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_manufacturer.cli_manufacturer_inputs import CLIManufacturerInputs
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.inventory.dao import DaoHost


class MenuHostNew(Menu):
    def __init__(self, console):
        super().__init__(
            console=console,
            path=CLIPaths.HOST_NEW.value
        )

    def start(self):
        try:
            new_host = CLIHostInputs.get_host(console=self.console)
            if not new_host:
                self.console.print("An unexpected error occurred. Can't add new host.", style=str(Color.FAIL.value))
                raise CLIHostInputs.InvalidAddressInformationException
            if new_host:
                DaoHost().add_host(
                    host=new_host
                )
                self.console.print(
                    Panel(f"The host {new_host.name} has been added successfully!",
                          title="Process completed!"),
                    style=str(Color.SUCCESS.value)
                )
        except (CLIHostInputs.InvalidAddressInformationException, CLIManufacturerInputs.NoManufacturersException):
            pass
        wait_for_user_to_continue(console=self.console)
