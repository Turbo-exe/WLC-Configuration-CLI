from rich.console import Console
from rich.panel import Panel

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_collection.cli_collection_inputs import CLICollectionInputs
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.configuration.dao.dao_collection import DaoCollection
from app.configuration.dao.dao_command_collection import DaoCommandCollection
from app.configuration.model.collection import Collection
from app.configuration.model.command_collection import CommandCollection


class MenuCollectionModify(Menu):
    def __init__(self, console: Console, collection: Collection):
        super().__init__(
            console=console,
            path=CLIPaths.HOST_MODIFY.value
        )
        self.collection = collection

    def start(self):
        modified_collection, modified_commands = CLICollectionInputs().get_collection_from_user(
            console=self.console,
            default_collection=self.collection
        )
        DaoCollection().modify_collection(
            collection=self.collection,
            id_=self.collection.id,
            name=modified_collection.name,
            description=modified_collection.description
        )
        try:
            command_collections = DaoCommandCollection().find_by_collection_id(collection_id=self.collection.id)
        except CommandCollection.NotFoundException:
            command_collections = []
        for command_collection in command_collections:
            DaoCommandCollection().delete_command_collection(command_collection)
        for i, command in enumerate(modified_commands):
            DaoCommandCollection().add_command_collection(
                command_collection=CommandCollection(
                    collection_id=self.collection.id,
                    command_id=command.id,
                    index=i
                )
            )
        self.console.print(
            Panel(f"The collection {modified_collection.name} has been modified successfully!",
                  title="Process completed!"),
            style=str(Color.SUCCESS.value)
        )
        wait_for_user_to_continue(console=self.console)
