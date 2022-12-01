from rich.text import Text

from app.cli.cli_components.menu import Menu
from app.cli.cli_components.selection import Selection
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_variables.information.modify.cli_variable_modify import \
    MenuVariableModify
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_variables.information.modify.cli_variable_remove import \
    MenuVariableRemove
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.configuration.model.variable import Variable


class MenuVariableInformation(Menu):
    def __init__(self, console, variable: Variable):
        super().__init__(
            console=console,
            path=CLIPaths.COMMANDS_INFORMATION.value
        )
        self.variable = variable
        self.text = Text.assemble(
            (f"\n{variable.name}\n\n", f"bold {Color.VARIABLE.value}"),
            f"Description: ",
            (f"{variable.description}\n", str(Color.VARIABLE.value)),
            f"Regex validation string: \n  ",
            (f"{variable.regex_string}\n", str(Color.VARIABLE.value))
        )
        self.options = {
            1: (MenuVariableModify(console=self.console, variable=self.variable), "name"),
            2: (MenuVariableRemove(console=self.console, variable=self.variable), "name"),
            99: (CLIPaths.BACK, "value")
        }

    def start(self):
        self.reset_screen()
        self.console.print(self.text)
        self.console.print("\n" * 2)
        self._setup_selection()
        option = self.selection_variable_modify_mode.start_selection()
        if self._selection_option_is_show_able(option=option):
            option.start()
        else:
            return

    def _setup_selection(self):
        self.selection_variable_modify_mode = Selection(
            prompt="Please select what you want to do",
            console=self.console
        )
        self.selection_variable_modify_mode.register_and_show_options(self.options)
