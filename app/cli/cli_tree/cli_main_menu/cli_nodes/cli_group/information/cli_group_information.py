from rich.columns import Columns
from rich.text import Text

from app.cli.cli_components.menu import Menu
from app.cli.cli_components.selection import Selection
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_group.information.modify.cli_group_modify import MenuGroupModify
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_group.information.modify.cli_group_remove import MenuGroupRemove
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_overview.cli_overview import MenuOverview
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.inventory.dao.dao_host import DaoHost
from app.inventory.model.group import Group


class MenuGroupInformation(Menu):
    def __init__(self, console, group: Group):
        super().__init__(
            console=console,
            path=CLIPaths.GROUPS_INFORMATION.value
        )
        self.group = group

        self.text = Text.assemble(
            (f"\n{group.name}\n\n", f"bold {Color.GROUP.value}"),
            f"Manufacturer: ",
            (f"{group.manufacturer_name}\n", str(Color.GROUP.value)),
            f"Host Count: ",
            (f"{len(group.hosts) if group.hosts else 0}", str(Color.HOST.value)),
        )

        hosts = DaoHost().get_hosts_for_node(node=group)
        self.text_hosts = "Hosts\n"
        if hosts:
            for host in hosts:
                self.text_hosts += f"[{Color.HOST.value}]  - {host.name}\n"
            self.text_hosts = self.text_hosts.rstrip("\n")
        else:
            self.text_hosts = ""
        self.options = {
            1: (MenuGroupModify(console=self.console, group=group), "name"),
            2: (MenuGroupRemove(console=self.console, group=group), "name"),
            99: (CLIPaths.BACK, "value")
        }

    def start(self):
        self.reset_screen()
        self.console.print(self.text)
        self.console.print(self.text_hosts)
        legend, trees = MenuOverview(
            console=self.console,
            nodes=[self.group, ]
        ).get_legend_and_tree()
        self.console.print("\n" * 2)
        self.console.print(Columns(trees))
        self.console.print("\n" * 2)
        self.console.print(legend)
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
