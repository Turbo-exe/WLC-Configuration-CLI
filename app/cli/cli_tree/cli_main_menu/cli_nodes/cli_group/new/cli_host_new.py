from rich.panel import Panel

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_group.cli_group_inputs import CLIGroupInputs
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_manufacturer.cli_manufacturer_inputs import CLIManufacturerInputs
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.inventory.dao import DaoGroup


class MenuGroupNew(Menu):
    def __init__(self, console):
        super().__init__(
            console=console,
            path=CLIPaths.GROUPS_NEW.value
        )

    def start(self):

        try:
            new_group = CLIGroupInputs.get_group(console=self.console)
            if not new_group:
                self.console.print("An unexpected error occurred. Can't add new group", style=str(Color.FAIL.value))
                raise CLIManufacturerInputs.NoManufacturersException
            DaoGroup().add_group_to_manufacturer(
                group=new_group
            )
            self.console.print(
                Panel(f"The group {new_group.name} has been added successfully!",
                      title="Process completed!"),
                style=str(Color.SUCCESS.value)
            )
        except CLIManufacturerInputs.NoManufacturersException:
            pass
        wait_for_user_to_continue(console=self.console)
