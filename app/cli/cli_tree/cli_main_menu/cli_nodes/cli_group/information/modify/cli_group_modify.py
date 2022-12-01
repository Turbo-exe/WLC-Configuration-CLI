from rich.console import Console
from rich.panel import Panel

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_group.cli_group_inputs import CLIGroupInputs
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_manufacturer.cli_manufacturer_inputs import CLIManufacturerInputs
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.inventory.dao import DaoGroup, DaoHost
from app.inventory.model.group import Group


class MenuGroupModify(Menu):
    def __init__(self, console: Console, group: Group):
        super().__init__(
            console=console,
            path=CLIPaths.GROUPS_MODIFY.value
        )

        self.group = group

    @staticmethod
    def _group_was_moved(original_group: Group, modified_group: Group) -> bool:
        return original_group.manufacturer_name.lower() != modified_group.manufacturer_name.lower()

    @staticmethod
    def _group_hosts_were_changed(original_group: Group, modified_group: Group):
        return original_group.hosts != modified_group.hosts

    @staticmethod
    def _get_added_hosts(original_group: Group, modified_group: Group):
        added_hosts = []
        if not original_group.hosts:
            original_group.hosts = []
        try:
            for host in modified_group.hosts:
                if host not in original_group.hosts:
                    added_hosts.append(host)
        except TypeError:
            pass
        return added_hosts

    @staticmethod
    def _get_removed_hosts(original_group: Group, modified_group: Group):
        removed_hosts = []
        if not modified_group.hosts:
            modified_group.hosts = []
        try:
            for host in original_group.hosts:
                if host not in modified_group.hosts:
                    removed_hosts.append(host)
        except TypeError:
            pass
        return removed_hosts

    def start(self):
        from app.inventory.model.host import Host
        try:
            modified_group = CLIGroupInputs.get_group(
                console=self.console,
                default_group=self.group
            )
        except CLIManufacturerInputs.NoManufacturersException:
            wait_for_user_to_continue(console=self.console)
            return

        DaoGroup().modify_group(
            original_group=self.group,
            modified_group=modified_group
        )

        if self._group_hosts_were_changed(original_group=self.group, modified_group=modified_group):
            added_hosts = self._get_added_hosts(original_group=self.group, modified_group=modified_group)
            removed_hosts = self._get_removed_hosts(original_group=self.group, modified_group=modified_group)
            for added_host in added_hosts:
                group_names = added_host.group_names.copy()
                if modified_group.name not in group_names:
                    group_names.append(modified_group.name)
                modified_host = Host(
                    manufacturer_name=added_host.manufacturer_name,
                    ipv4_address=added_host.ipv4_address,
                    ipv6_address=added_host.ipv6_address,
                    fqdn=added_host.fqdn,
                    name=added_host.name,
                    group_names=group_names
                )
                DaoHost.modify_host(
                    original_host=added_host,
                    modified_host=modified_host,
                    send_add=False,
                    send_remove=False
                )
                modified_group.hosts.remove(added_host)
                modified_group.hosts.append(modified_host)
            for removed_host in removed_hosts:
                try:
                    group_names = removed_host.group_names.copy()
                    group_names.remove(modified_group.name)
                except ValueError:
                    group_names = []
                modified_host = Host(
                    manufacturer_name=removed_host.manufacturer_name,
                    ipv4_address=removed_host.ipv4_address,
                    ipv6_address=removed_host.ipv6_address,
                    fqdn=removed_host.fqdn,
                    name=removed_host.name,
                    group_names=group_names
                )
                if modified_group.name not in modified_host.group_names:
                    DaoHost.modify_host(original_host=removed_host,
                                        modified_host=modified_host,
                                        send_add=False,
                                        send_remove=False)
                    self.group.hosts.remove(removed_host)
        self.console.print(
            Panel(f"The group {modified_group.name}"
                  f"{' (Previously: ' + self.group.name + ')' if modified_group.name != self.group.name else ''} "
                  f"has been modified successfully!",
                  title="Process completed!"),
            style=str(Color.SUCCESS.value)
        )
        wait_for_user_to_continue(console=self.console)
