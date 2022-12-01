from rich.columns import Columns
from rich.text import Text

from app.cli.cli_components.menu import Menu
from app.cli.cli_components.selection import Selection
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_host.information.modify.cli_host_modify import MenuHostModify
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_host.information.modify.cli_host_remove import MenuHostRemove
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_overview.cli_overview import MenuOverview
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.inventory.model.host import Host


class MenuHostInformation(Menu):
    def __init__(self, console, host: Host):
        super().__init__(
            console=console,
            path=CLIPaths.HOST_INFORMATION.value
        )
        self.host = host
        self.host_info = (
            f""
            f"IPv4 address: '{host.ipv4_address}'\n"
            f"IPV6 address: '{host.ipv6_address}'"
            f"Fully qualified domain name: '{host.fqdn}'"

        )

        self.text = Text.assemble(
            (f"\n{host.name}\n\n", f"bold {Color.HOST.value}"),
            f"IPv4 address: ",
            (f"{host.ipv4_address}\n", str(Color.HOST.value)),
            f"IPv6 address: ",
            (f"{host.ipv6_address}\n", str(Color.HOST.value)),
            f"Fully qualified domain name: ",
            (f"{host.fqdn}\n", str(Color.HOST.value)),
            f"Manufacturer: ",
            (f"{host.manufacturer_name}\n", str(Color.HOST.value)),
        )

        self.options = {
            1: (MenuHostModify(console=self.console, host=host), "name"),
            2: (MenuHostRemove(console=self.console, host=host), "name"),
            99: (CLIPaths.BACK, "value")
        }

    def start(self):
        self.reset_screen()
        legend, trees = MenuOverview(
            console=self.console,
            nodes=[self.host, ]
        ).get_legend_and_tree()
        self.console.print(self.text)
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
