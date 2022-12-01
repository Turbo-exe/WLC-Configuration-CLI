from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns

from app.cli.cli_components.menu import Menu
from app.cli.cli_components.selection import Selection
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_manufacturer.information.modify.cli_manufacturer_rename import \
    MenuManufacturerRename
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_manufacturer.information.modify.cli_manufacturer_remove import \
    MenuManufacturerRemove
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_overview.cli_overview import MenuOverview
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.inventory.dao import DaoGroup
from app.inventory.dao.dao_host import DaoHost
from app.inventory.dao import DaoManufacturer

from app.inventory.model.group import Group
from app.inventory.model.manufacturer import Manufacturer


class ManufacturerInformation(Menu):
    def __init__(self, console, manufacturer_name):
        super().__init__(
            console=console,
            path=CLIPaths.MANUFACTURER_INFORMATION.value
        )
        manufacturer = DaoManufacturer().get_manufacturer_by_name(manufacturer_name=manufacturer_name)
        self.manufacturer = manufacturer
        self.text = Text.assemble(
            (f"\n{manufacturer.name}\n\n", f"bold {Color.MANUFACTURER.value}"),
            f"Group Count: ",
            (f"{len(manufacturer.children) if manufacturer.children else 0}", str(Color.GROUP.value)),
        )
        groups = DaoGroup.get_groups_for_node(node=manufacturer)
        self.text_groups = "Groups:\n"
        if groups:
            for group in groups:
                self.text_groups += f"[{Color.GROUP.value}]  - {group.name}\n"
            self.text_groups = self.text_groups.rstrip("\n")
        else:
            self.text_groups = ""

        hosts = DaoHost().get_hosts_for_node(node=manufacturer)
        self.text_host_count = Text.assemble(
            f"Host Count: ",
            (f"{len(hosts) if hosts else 0}", str(Color.HOST.value)),)
        self.text_hosts = "Hosts\n"
        if hosts:
            for host in hosts:
                self.text_hosts += f"[{Color.HOST.value}]  - {host.name}\n"
            self.text_hosts = self.text_hosts.rstrip("\n")
        else:
            self.text_hosts = ""

        self.options = {
            1: (MenuManufacturerRename(console=self.console, manufacturer=manufacturer), "name"),
            2: (MenuManufacturerRemove(console=self.console, manufacturer=manufacturer), "name"),
            99: (CLIPaths.BACK, "value")
        }

    def start(self):
        self.reset_screen()
        self.console.print(self.text)
        self.console.print(self.text_groups)
        self.console.print(self.text_host_count)
        self.console.print(self.text_hosts)
        legend, trees = MenuOverview(
            console=self.console,
            nodes=[self.manufacturer, ]
        ).get_legend_and_tree()
        self.console.print("\n" * 2)
        self.console.print(Columns(trees))
        self.console.print("\n" * 2)
        self.console.print(legend)
        self.console.print("\n" * 2)
        self._setup_selection()
        option = self.selection_manufacturer_modify_mode.start_selection()
        if self._selection_option_is_show_able(option=option):
            option.start()
        else:
            return

    def _setup_selection(self):
        self.selection_manufacturer_modify_mode = Selection(
            prompt="Please select what you want to do",
            console=self.console
        )
        self.selection_manufacturer_modify_mode.register_and_show_options(self.options)

    @staticmethod
    def _general_panel(manufacturer: Manufacturer):
        groups = DaoGroup().get_groups_for_node(
            node=manufacturer
        )

        text = f"NAME: {manufacturer.name}\n"
        if groups:
            text += "GROUPS:\n"
            for group in groups:
                text += f"  - {group.name}\n"
        text = text.rstrip("\n")

        return Panel(
            Text(
                text=text
            ),
            title="General"
        )

    @staticmethod
    def _hosts_panel(manufacturer: Manufacturer):
        hosts = DaoHost().get_hosts_for_node(node=manufacturer)
        text = ""
        if hosts:
            for host in hosts:
                text += f"  - {host.name}\n"
            text = text.rstrip("\n")
        else:
            text = "No hosts by this manufacturer"
        return Panel(
            Text(
                text=text
            ),
            title="All hosts"
        )

    def _groups_panels(self, manufacturer: Manufacturer):
        groups = DaoGroup().get_groups_for_node(
            node=manufacturer
        )
        panels = []
        if groups:
            for group in groups:
                panels.append(self._groups_panel(group=group))
        return panels

    @staticmethod
    def _groups_panel(group: Group):
        hosts = group.hosts

        text = ""
        if hosts:
            for host in hosts:
                text += f"  - {host.name}\n"
            text = text.rstrip("\n")
        else:
            text = "No hosts in this group"
        return Panel(
            Text(
                text=text
            ),
            title=f"Hosts in Group \"{group.name}\""
        )
