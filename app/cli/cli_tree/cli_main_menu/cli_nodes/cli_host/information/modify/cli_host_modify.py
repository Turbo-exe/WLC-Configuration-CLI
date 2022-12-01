from rich.console import Console
from rich.panel import Panel

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_host.cli_host_inputs import CLIHostInputs
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_manufacturer.cli_manufacturer_inputs import CLIManufacturerInputs
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.inventory.dao import DaoHost
from app.inventory.model.host import Host


class MenuHostModify(Menu):
    def __init__(self, console: Console, host: Host):
        super().__init__(
            console=console,
            path=CLIPaths.HOST_MODIFY.value
        )
        self.host = host

    def start(self):
        try:
            modified_host = CLIHostInputs.get_host(
                console=self.console,
                default_host=self.host
            )
            DaoHost().modify_host(
                original_host=self.host,
                modified_host=modified_host
            )
            self.console.print(
                Panel(f"The host {modified_host.name}"
                      f"{' (Previously: ' + self.host.name + ')' if modified_host.name != self.host.name else ''} "
                      f" has been modified successfully!",
                      title="Process completed!"),
                style=str(Color.SUCCESS.value)
            )
        except (CLIHostInputs.InvalidAddressInformationException, CLIManufacturerInputs.NoManufacturersException):
            pass
        wait_for_user_to_continue(console=self.console)

    def is_valid_address_information(self, ipv4_address: str, ipv6_address: str, fqdn: str):
        try:
            Host.check_if_address_information_is_provided(
                ipv4_address=ipv4_address,
                ipv6_address=ipv6_address,
                fqdn=fqdn
            )
            return True
        except Host.NoAddressException:
            self.console.print(
                Panel("The entered information is invalid. Couldn't find any address information. "
                      "You must at least specify one address for modifying this host.",
                      title="Process aborted!"),
                style=str(Color.FAIL.value))
            return False
