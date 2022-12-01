from rich.text import Text

from app.cli.cli_components.menu import Menu
from app.cli.cli_components.selection import Selection
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_command.information.modify.cli_command_modify import \
    MenuCommandModify
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_command.information.modify.cli_command_remove import \
    MenuCommandRemove
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.configuration.dao.dao_command_line import DaoCommandLine
from app.configuration.model.command import Command


class MenuCommandInformation(Menu):
    def __init__(self, console, command: Command):
        super().__init__(
            console=console,
            path=CLIPaths.COMMANDS_INFORMATION.value
        )
        self.command = command
        lines = "\n  ".join(
            [cmd_line.command_line for cmd_line in DaoCommandLine().find_by_command_id(command_id=command.id)]
        )
        self.text = Text.assemble(
            (f"\n{command.name}\n\n", f"bold {Color.COMMAND.value}"),
            f"Description: ",
            (f"{command.description}\n", str(Color.COMMAND.value)),
            f"Command: \n  ",
            (f"{lines}\n", str(Color.COMMAND.value))
        )

        self.options = {
            1: (MenuCommandModify(console=self.console, command=self.command), "name"),
            2: (MenuCommandRemove(console=self.console, command=self.command), "name"),
            99: (CLIPaths.BACK, "value")
        }

    def start(self):
        self.reset_screen()
        self.console.print(self.text)
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
