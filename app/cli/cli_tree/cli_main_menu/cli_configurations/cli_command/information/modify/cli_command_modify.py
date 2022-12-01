from rich.console import Console
from rich.panel import Panel

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_command.cli_command_input import CLICommandInputs
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.configuration.dao.dao_command import DaoCommand
from app.configuration.dao.dao_command_line import DaoCommandLine
from app.configuration.model.command import Command


class MenuCommandModify(Menu):
    def __init__(self, console: Console, command: Command):
        super().__init__(
            console=console,
            path=CLIPaths.COMMANDS_MODIFY.value
        )
        self.command = command

    def start(self):
        modified_command, modified_command_lines = CLICommandInputs().get_command_from_user(
            console=self.console,
            default_command=self.command
        )
        DaoCommand().modify_command(
            command=self.command,
            id_=modified_command.id,
            name=modified_command.name,
            description=modified_command.description
        )
        original_command_lines = DaoCommandLine().find_by_command_id(command_id=self.command.id)
        for i, modified_command_line in enumerate(modified_command_lines):
            if i + 1 <= len(original_command_lines):
                DaoCommandLine().modify_command_line(
                    command_line=modified_command_line,
                    id_=modified_command_line.id,
                    command_id=modified_command.id,
                    command_line_=modified_command_line.command_line
                )
            else:
                DaoCommandLine().add_command_line(command_line=modified_command_line)
        self.console.print(
            Panel(f"The command {modified_command.name} has been modified successfully!",
                  title="Process completed!"),
            style=str(Color.SUCCESS.value)
        )
        wait_for_user_to_continue(console=self.console)
