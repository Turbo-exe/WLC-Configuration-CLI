from rich.console import Console
from rich.panel import Panel

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.cli_components.yes_no import YesNo
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.inventory.dao import DaoHost
from app.inventory.model.host import Host


class MenuHostRemove(Menu):
    def __init__(self, console: Console, host: Host):
        super().__init__(
            console=console,
            path=CLIPaths.HOST_REMOVE.value
        )
        self.host = host

    def start(self):
        if YesNo(console=self.console,
                 prompt=f"Are you sure that you want to delete the host '{self.host.name}'?"
                        " This cannot be undone!").decision:

            DaoHost().remove_host(
                host=self.host
            )
            self.console.print(
                Panel(f"The host '{self.host.name}' has been deleted successfully!",
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
