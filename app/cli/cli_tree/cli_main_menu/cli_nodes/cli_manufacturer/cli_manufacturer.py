from rich.panel import Panel

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_manufacturer.information.cli_manufacturer_information import ManufacturerInformation
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_manufacturer.new.cli_manufacturer_new import MenuManufacturerNew
from app.cli.enum.cli_options import CLIPaths
from app.cli.cli_components.selection import Selection
from app.inventory.dao import DaoManufacturer


class MenuManufacturer(Menu):
    def __init__(self, console, prompt="Please select a WLC-Manufacturer",
                 show_new_option=True, show_back_option=True, allow_empty_selection=False):
        super().__init__(
            console=console,
            path=CLIPaths.MANUFACTURER.value
        )
        self.selection_manufacturer = None
        self.show_new_option = show_new_option
        self.show_back_option = show_back_option
        self.manufacturers = {}
        self.manufacturers.clear()
        self.prompt = prompt
        self.allow_empty_selection = allow_empty_selection

    def _load_options(self):
        manufacturers = DaoManufacturer().get_manufacturers()
        if manufacturers:
            for manufacturer in manufacturers:
                self._add_manufacturer_selection(manufacturer=manufacturer.name)
        if self.show_new_option:
            self._add_new_option()
        if self.show_back_option:
            self._add_back_option()

    def _add_back_option(self):
        if self.manufacturers:
            if max(self.manufacturers) < 99:
                index = 99
            else:
                index = max(self.manufacturers) + 1
        else:
            index = 99
        self.manufacturers.setdefault(index, (CLIPaths.BACK, "value"))

    def _add_new_option(self):
        if self.manufacturers:
            index = max(self.manufacturers) + 1
        else:
            index = 1
        self.manufacturers.setdefault(index, (MenuManufacturerNew(console=self.console), "name"))

    def _add_manufacturer_selection(self, manufacturer: str) -> int:
        index = 1
        if self.manufacturers:
            index = max(self.manufacturers) + 1
        self.manufacturers.setdefault(
            index,
            (ManufacturerInformation(console=self.console, manufacturer_name=manufacturer), manufacturer)
        )
        return index

    def _setup_manufacturer_selection(self):
        self.selection_manufacturer = Selection(prompt=self.prompt, console=self.console)
        self.selection_manufacturer.register_and_show_options(self.manufacturers)

    def start(self, reset_screen=True, return_manufacturer=False):
        if reset_screen:
            self.reset_screen()
        self._load_options()
        self._setup_manufacturer_selection()
        selection = self.selection_manufacturer.start_selection(allow_empty_selection=self.allow_empty_selection)
        if reset_screen:
            self.horizontal_spacer()
        if return_manufacturer:
            return selection
        else:
            self._decide_upon_selection(selected_option=selection)

    def _decide_upon_selection(self, selected_option):
        self.manufacturers.clear()
        super()._decide_upon_selection(selected_option=selected_option)
