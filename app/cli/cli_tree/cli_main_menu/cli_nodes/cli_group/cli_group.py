from app.cli.cli_components.menu import Menu
from app.cli.cli_components.selection import Selection
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_group.information.cli_group_information import MenuGroupInformation
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_group.new.cli_host_new import MenuGroupNew
from app.cli.enum.cli_options import CLIPaths
from app.inventory.dao import DaoGroup
from app.inventory.model.group import Group


class MenuGroup(Menu):
    def __init__(self, console, prompt="Please select a group", show_new_option=True):
        super().__init__(
            console=console,
            path=CLIPaths.GROUPS.value
        )
        self.selection_group = None
        self.show_new_option = show_new_option
        self.groups = {}
        self.groups.clear()
        self.prompt = prompt

    def _load_options(self):
        groups = DaoGroup().get_all_groups()
        if groups:
            for group in groups:
                self._add_group_selection(group=group)
        if self.show_new_option:
            self._add_new_option()
        self._add_back_option()

    def _add_back_option(self):
        if self.groups:
            if max(self.groups) < 99:
                index = 99
            else:
                index = max(self.groups) + 1
        else:
            index = 99
        self.groups.setdefault(index, (CLIPaths.BACK, "value"))

    def _add_new_option(self):
        if self.groups:
            index = max(self.groups) + 1
        else:
            index = 1
        self.groups.setdefault(index, (MenuGroupNew(console=self.console), "name"))

    def _add_group_selection(self, group: Group) -> int:
        index = 1
        if self.groups:
            index = max(self.groups) + 1
        self.groups.setdefault(
            index,
            (MenuGroupInformation(console=self.console, group=group), f"{group.name} - {group.manufacturer_name}")
        )
        return index

    def _setup_group_selection(self):
        self.selection_group = Selection(prompt=self.prompt, console=self.console)
        self.selection_group.register_and_show_options(self.groups)

    def _is_manufacturer(self, input_val):
        for key, item in self.groups.items():
            if isinstance(item, tuple):
                if input_val in item:
                    return item
            if input_val == item or input_val == key:
                return item
        return False

    def start(self):
        self.reset_screen()
        self._load_options()
        self._setup_group_selection()
        selection = self.selection_group.start_selection()
        self.horizontal_spacer()
        self._decide_upon_selection(selected_option=selection)

    def _decide_upon_selection(self, selected_option):
        self.groups.clear()
        super()._decide_upon_selection(selected_option=selected_option)
