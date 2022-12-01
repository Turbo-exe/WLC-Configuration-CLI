from app.cli.cli_components.menu import Menu
from app.cli.cli_components.selection import Selection
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_configurations import MenuConfigurations
from app.cli.cli_tree.cli_main_menu.cli_execute.cli_execute import MenuExecute
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_nodes import MenuNodes
from app.cli.enum.cli_options import CLIPaths, CLIOptions


class MenuMainMenu(Menu):
    def __init__(self, console):
        super().__init__(
            console=console,
            path=CLIPaths.MAIN_MENU.value
        )
        self.selection = None
        self.console = console

    def start(self):
        self.reset_screen()
        options = {
            1: (MenuNodes(console=self.console), "name"),
            2: (MenuConfigurations(console=self.console), "name"),
            3: (MenuExecute(console=self.console), "name"),
            99: (CLIOptions.CLOSE, "value")
        }
        main_menu_selection = Selection(prompt="Please select what you want to do", console=self.console)
        main_menu_selection.register_and_show_options(options=options)
        self.selection = main_menu_selection.start_selection()
        if self.selection == CLIOptions.CLOSE:
            exit()
        self.selection.start()
        self.start()
