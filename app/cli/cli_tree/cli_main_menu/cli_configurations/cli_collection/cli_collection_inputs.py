from rich.console import Console

from app.cli.cli_components.multiselection import MultiSelection
from app.cli.cli_components.user_input import UserInput
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_command.cli_command_input import CLICommandInputs
from app.cli.enum.color import Color
from app.configuration.dao.dao_collection import DaoCollection
from app.configuration.dao.dao_command import DaoCommand
from app.configuration.dao.dao_command_collection import DaoCommandCollection
from app.configuration.model.collection import Collection
from app.configuration.model.command import Command
from app.configuration.model.command_collection import CommandCollection


class CLICollectionInputs:
    @staticmethod
    def _inform_user(console):
        console.print("Please enter the following requested information about the new collection.\n")
        console.print("\nIdentification", style=str(Color.COMMAND.value))

    @staticmethod
    def _default_values(default_collection: Collection) -> tuple[str, str]:
        if default_collection:
            return \
                f"{default_collection.name}", \
                f"{default_collection.description}"
        else:
            return ("",) * 2

    def get_collection_from_user(self, console, default_collection: Collection = None) \
            -> tuple[Collection, list[Command]]:
        try:
            default_name, default_description = self._default_values(
                default_collection=default_collection
            )
            self._inform_user(console=console)
            name = UserInput(console=console, prompt="Name", default_answer=default_name,
                             mandatory=True, validate_func=Collection.validate_name).answer
            description = UserInput(console=console, prompt="Description", default_answer=default_description,
                                    mandatory=False, validate_func=Collection.validate_description).answer
            default_commands = []
            default_collection_id = None
            if default_collection:
                try:
                    command_collections = DaoCommandCollection().find_by_collection_id(collection_id=default_collection.id)
                    for command_collection in command_collections:
                        default_commands.append(DaoCommand().find_by_command_id(command_collection.command_id))
                    default_collection_id = default_collection.id
                except CommandCollection.NotFoundException:
                    pass
            commands = CLICommandInputs.choose_from_commands(console=console, default_commands=default_commands,
                                                             collection_id=default_collection_id)

            return Collection(
                name=name,
                description=description
            ), commands
        except RecursionError:
            console.print("To many recursions. Aborting process...")

    @staticmethod
    def choose_from_collections(console: Console, collections=None, numbered=False) -> list[Collection]:
        if not collections:
            collections = DaoCollection().find_all_collections()
        options = {}
        for cmd in collections:
            if not options:
                index = 1
            else:
                index = max(options) + 1
            options.setdefault(index, (cmd, cmd.name, -1))
        if options:
            collection_selection = MultiSelection(prompt="Collection Selection", console=console, numbered=numbered)
            collection_selection.register_and_show_options(
                options=options
            )
            collections_and_selections = collection_selection.start_selection()
            return_val = []
            for collection, is_selected in collections_and_selections:
                if is_selected != -1:
                    return_val.append(collection)
            return return_val
        else:
            console.print("No collections found. Skipping collection selection...")
            return []
