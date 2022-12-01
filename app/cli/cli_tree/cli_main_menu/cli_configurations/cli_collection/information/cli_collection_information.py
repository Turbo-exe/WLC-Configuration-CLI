from rich.table import Table, Column
from rich.text import Text

from app.cli.cli_components.menu import Menu
from app.cli.cli_components.selection import Selection
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_collection.information.modify.cli_collection_modify import \
    MenuCollectionModify
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_collection.information.modify.cli_collection_remove import \
    MenuCollectionRemove
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.configuration.dao.dao_command import DaoCommand
from app.configuration.dao.dao_command_collection import DaoCommandCollection
from app.configuration.dao.dao_command_line import DaoCommandLine
from app.configuration.model.collection import Collection
from app.configuration.model.command_collection import CommandCollection
from app.configuration.service.service_command_collection import ServiceCommandCollection


class MenuCollectionInformation(Menu):
    def __init__(self, console, collection: Collection):
        super().__init__(
            console=console,
            path=CLIPaths.COLLECTIONS_INFORMATION.value
        )
        self.collection = collection
        try:
            self.commands_for_collection = ServiceCommandCollection().get_commands_by_collection_id(collection.id)
        except CommandCollection.NotFoundException:
            self.commands_for_collection = []
        self.table = Table(
            Column(
                header="Step No.", width=8
            ),
            Column(
                header="Name"
            ),
            Column(
                header="Description"
            ),
            Column(
                header="Command(s)"
            )
        )
        for command in self.commands_for_collection:
            command_collection = DaoCommandCollection().find_by_command_id_and_collection_id(
                command_id=command.id,
                collection_id=self.collection.id
            )
            self.table.add_row(
                str(command_collection.index + 1),
                command.name,
                command.description,
                '\n'.join([cmd_line.command_line for cmd_line in DaoCommandLine().find_by_command_id(
                    command_id=command.id
                )])
            )
            self.table.add_row("")
        self.text = Text.assemble(
            (f"\n{collection.name}\n\n", f"bold {Color.COLLECTION.value}"),
            f"Description: ",
            (f"{collection.description}\n", str(Color.COLLECTION.value)),
            f"Command Count: ",
            (f"{len(self.commands_for_collection)}\n", str(Color.COLLECTION.value)),
            f"Commands: "
        )

        self.options = {
            1: (MenuCollectionModify(console=self.console, collection=self.collection), "name"),
            2: (MenuCollectionRemove(console=self.console, collection=self.collection), "name"),
            99: (CLIPaths.BACK, "value")
        }

    def start(self):
        self.reset_screen()
        self.console.print(self.text)
        self.console.print(self.table)
        self.console.print("\n" * 2)
        self._setup_selection()
        option = self.selection_collection_modify_mode.start_selection()
        if self._selection_option_is_show_able(option=option):
            option.start()
        else:
            return

    def _setup_selection(self):
        self.selection_collection_modify_mode = Selection(
            prompt="Please select what you want to do",
            console=self.console
        )
        self.selection_collection_modify_mode.register_and_show_options(self.options)
