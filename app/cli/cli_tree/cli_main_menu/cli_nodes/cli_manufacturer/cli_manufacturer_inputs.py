from rich.console import Console

from app.cli.cli_components.menu import Menu
from app.cli.cli_components.multiselection import MultiSelection
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_manufacturer.cli_manufacturer import MenuManufacturer
from app.inventory.dao import DaoManufacturer
from app.inventory.model.manufacturer import Manufacturer


class CLIManufacturerInputs:
    @staticmethod
    def get_manufacturer(console: Console, prompt: str, default: str = ""):
        if not DaoManufacturer.get_manufacturers():
            raise CLIManufacturerInputs.NoManufacturersException
        if default:
            _prompt = f"{prompt} (default={default}): "
        else:
            _prompt = prompt + ":"
        manufacturer = MenuManufacturer(
            console=console,
            prompt=_prompt,
            show_new_option=False,
            show_back_option=False,
            allow_empty_selection=True if default else False
        ).start(reset_screen=False, return_manufacturer=True)
        if manufacturer:
            manufacturer = manufacturer.manufacturer
        if default and not manufacturer:
            manufacturer = DaoManufacturer.get_manufacturer_by_name(default.replace("'", ""))
        Menu.clear_last_line(len_last_line=len(_prompt) + len(manufacturer.name) * 3)
        console.print(f"{prompt}: {manufacturer.name}")
        return manufacturer

    @staticmethod
    def choose_from_manufacturers(console: Console, manufacturers: list[Manufacturer] = None):
        if not manufacturers:
            manufacturers = DaoManufacturer().get_manufacturers()
        options = {}
        for manufacturer in manufacturers:
            if not options:
                index = 1
            else:
                index = max(options) + 1
            options.setdefault(index, (manufacturer, manufacturer.name, -1))

        manufacturer_selection = MultiSelection(prompt="Manufacturer Selection", console=console)
        manufacturer_selection.register_and_show_options(
            options=options
        )
        manufacturers_and_selections = manufacturer_selection.start_selection()
        return_val = []
        for manufacturer, is_selected in manufacturers_and_selections:
            if is_selected != -1:
                return_val.append(manufacturer)
        return return_val

    class NoManufacturersException(Exception):
        pass
