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
from app.configuration.dao.dao_command_collection import DaoCommandCollection
from app.configuration.model.command_collection import CommandCollection


class MenuCollectionNew(Menu):
    def __init__(self, console):
        super().__init__(
            console=console,
            path=CLIPaths.COLLECTIONS_NEW.value
        )

    def start(self):
        new_command_collection, new_commands = CLICollectionInputs().get_collection_from_user(console=self.console)

        if new_command_collection:
            DaoCollection().add_collection(
                collection=new_command_collection,
            )
            for command in new_commands:
                DaoCommandCollection().add_command_collection(
                    command_collection=CommandCollection(
                        collection_id=new_command_collection.id,
                        command_id=command.id,
                        index=0
                    )
                )
            self.console.print(
                Panel(f"The command collection {new_command_collection.name} has been added successfully!",
                      title="Process completed!"),
                style=str(Color.SUCCESS.value)
            )
        else:
            self.console.print(
                Panel(f"Something went wrong! Can't add a new command collection",
                      title="Process aborted!"),
                style=str(Color.FAIL.value)
            )

        wait_for_user_to_continue(console=self.console)
