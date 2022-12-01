from rich.panel import Panel

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_collection.cli_collection_inputs import \
    CLICollectionInputs
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_command.cli_command_input import \
    CLICommandInputs
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.configuration.dao.dao_collection import DaoCollection
from app.configuration.dao.dao_command import DaoCommand
from app.configuration.dao.dao_command_collection import DaoCommandCollection
from app.configuration.dao.dao_command_line import DaoCommandLine
from app.configuration.model.command_collection import CommandCollection


class MenuCommandNew(Menu):
    def __init__(self, console):
        super().__init__(
            console=console,
            path=CLIPaths.COMMANDS_NEW.value
        )

    def start(self):
        new_command, new_command_lines = CLICommandInputs().get_command_from_user(console=self.console)
        if new_command:
            DaoCommand().add_command(
                command=new_command
            )
            for command_line in new_command_lines:
                command_line.command_id = new_command.id
                DaoCommandLine().add_command_line(command_line=command_line)
            for collection in CLICollectionInputs().choose_from_collections(console=self.console):
                DaoCommandCollection().add_command_collection(CommandCollection(
                    collection_id=collection.id,
                    command_id=new_command.id,
                    index=0
                    )
                )
            self.console.print(
                Panel(f"The command {new_command.name} has been added successfully!",
                      title="Process completed!"),
                style=str(Color.SUCCESS.value)
            )
        else:
            self.console.print(
                Panel(f"Something went wrong. Can't add a new command!",
                      title="Process aborted!"),
                style=str(Color.FAIL.value)
            )
        wait_for_user_to_continue(console=self.console)
