from rich.console import Console
from rich.panel import Panel

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.cli_components.yes_no import YesNo
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.configuration.dao.dao_command import DaoCommand
from app.configuration.dao.dao_command_collection import DaoCommandCollection
from app.configuration.dao.dao_command_line import DaoCommandLine
from app.configuration.model.command import Command
from app.configuration.model.command_collection import CommandCollection


class MenuCommandRemove(Menu):
    def __init__(self, console: Console, command: Command):
        super().__init__(
            console=console,
            path=CLIPaths.COMMANDS_REMOVE.value
        )
        self.command = command

    def start(self):
        if YesNo(console=self.console,
                 prompt=f"Are you sure that you want to delete the command '{self.command.name}'?"
                        " This cannot be undone!").decision:

            DaoCommand().delete_command(
                command=self.command
            )

            for command_line in DaoCommandLine().find_by_command_id(command_id=self.command.id):
                DaoCommandLine().delete_command_line(
                    command_line=command_line
                )
            try:
                for command_collection in DaoCommandCollection().find_by_command_id(command_id=self.command.id):
                    DaoCommandCollection().delete_command_collection(
                        command_collection=command_collection
                    )
            except CommandCollection.NotFoundException:
                pass
            self.console.print(
                Panel(f"The command '{self.command.name}' has been deleted successfully!",
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
