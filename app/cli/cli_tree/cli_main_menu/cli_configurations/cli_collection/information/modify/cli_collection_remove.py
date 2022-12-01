from rich.console import Console
from rich.panel import Panel

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.cli_components.yes_no import YesNo
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.configuration.dao.dao_collection import DaoCollection
from app.configuration.model.collection import Collection


class MenuCollectionRemove(Menu):
    def __init__(self, console: Console, collection: Collection):
        super().__init__(
            console=console,
            path=CLIPaths.COMMANDS_REMOVE.value
        )
        self.collection = collection

    def start(self):
        if YesNo(console=self.console,
                 prompt=f"Are you sure that you want to delete the collection '{self.collection.name}'?"
                        " This cannot be undone!").decision:

            DaoCollection().delete_collection(
                collection=self.collection
            )
            self.console.print(
                Panel(f"The collection '{self.collection.name}' has been deleted successfully!",
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
