from app.cli.cli_components.menu import Menu
from app.cli.cli_components.selection import Selection
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_group.cli_group import MenuGroup
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_host.cli_host import MenuHost
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_manufacturer.cli_manufacturer import MenuManufacturer
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_overview.cli_overview import MenuOverview
from app.cli.enum.cli_options import CLIPaths


class MenuNodes(Menu):
    def __init__(self, console):
        super().__init__(
            console=console,
            path=CLIPaths.NODES.value
        )
        self.selection = None
        self.console = console

    def start(self):
        self.reset_screen()
        options = {
            1: (MenuOverview(console=self.console), "name"),
            2: (MenuManufacturer(console=self.console), "name"),
            3: (MenuGroup(console=self.console), "name"),
            4: (MenuHost(console=self.console), "name"),
            99: (CLIPaths.BACK, "value")
        }
        selection_component = Selection(prompt="Please select what you want to do", console=self.console)
        selection_component.register_and_show_options(options=options)
        option = selection_component.start_selection()
        self._decide_upon_selection(selected_option=option)
