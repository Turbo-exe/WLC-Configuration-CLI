from rich.console import Console
from rich.panel import Panel

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.cli_components.yes_no import YesNo
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.inventory.dao import DaoGroup
from app.inventory.model.group import Group


class MenuGroupRemove(Menu):
    def __init__(self, console: Console, group: Group):
        super().__init__(
            console=console,
            path=CLIPaths.GROUPS_REMOVE.value
        )
        self.group = group

    def start(self):
        if YesNo(console=self.console,
                 prompt=f"Are you sure that you want to delete the group '{self.group.name}'?"
                        " This cannot be undone!").decision:

            DaoGroup.remove_group_from_manufacturer(
                group=self.group
            )
            self.console.print(
                Panel(f"The group '{self.group.name}' has been deleted successfully!",
                      title="Process completed!"),
                style="green"
            )
        else:
            self.console.print(
                Panel(f"The process has been aborted!",
                      title="Process aborted!"),
                style=str(Color.FAIL.value)
            )
        wait_for_user_to_continue(console=self.console)
