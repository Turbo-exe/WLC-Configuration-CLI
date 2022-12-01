from app.cli.cli_components.menu import Menu
from app.cli.cli_components.selection import Selection
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_collection.cli_collection import \
    MenuCollection
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_command.cli_command import MenuCommand
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_variables.cli_variable import MenuVariable
from app.cli.enum.cli_options import CLIPaths


class MenuConfigurations(Menu):
    def __init__(self, console):
        super().__init__(
            console=console,
            path=CLIPaths.CONFIGURATIONS.value
        )
        self.selection = None
        self.console = console

    def start(self):
        self.reset_screen()
        options = {
            1: (MenuCommand(console=self.console), "name"),
            2: (MenuCollection(console=self.console), "name"),
            3: (MenuVariable(console=self.console), "name"),
            99: (CLIPaths.BACK, "value")
        }
        selection_component = Selection(prompt="Please select what you want to do", console=self.console)
        selection_component.register_and_show_options(options=options)
        option = selection_component.start_selection()
        self._decide_upon_selection(selected_option=option)
