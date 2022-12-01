from app.cli.util.list_utils import remove_duplicates
from app.inventory.dao import DaoManufacturer
from app.inventory.file.inventory import Inventory
from app.inventory.model.group import Group
from app.inventory.model.host import Host
from app.inventory.model.manufacturer import Manufacturer


class DaoHost:
    def get_hosts_for_node(self, node: Manufacturer or Group, recursive: bool = False) -> list[Host]:
        try:
            hosts = node.hosts.copy()
        except AttributeError:
            hosts = []
        if node.children:
            for parent in node.children:
                if parent.hosts:
                    try:
                        hosts.extend(list(parent.hosts))
                    except AttributeError:
                        pass
                if parent.children is not None and recursive:
                    hosts.extend(self.get_hosts_for_node(node=parent))
            hosts = remove_duplicates(input_list=hosts)
        return hosts

    def get_all_hosts(self) -> list[Host]:
        hosts = []
        for manufacturer in DaoManufacturer().get_manufacturers():
            if (new_hosts := self.get_hosts_for_node(manufacturer, recursive=True)) is not None:
                hosts.extend(new_hosts)
        return hosts

    @staticmethod
    def get_occurrences_of_host_in_node(host, parent) -> int:
        occurrences = 0
        if parent.children:
            for child in parent.children:
                occurrences += DaoHost.get_occurrences_of_host_in_node(host=host, parent=child)
        if parent.hosts:
            if host in parent.hosts:
                occurrences += 1
        return occurrences

    @staticmethod
    def add_host(host: Host, send: bool = True) -> None:
        with Inventory().readwrite(send=send) as inventory:
            for i, m in enumerate(inventory.manufacturers):
                if m.name == host.manufacturer_name:
                    if not host.group_names:
                        if inventory.manufacturers[i].hosts is None:
                            inventory.manufacturers[i].hosts = []
                        inventory.manufacturers[i].hosts.append(host)
                    else:
                        if m.children:
                            for o, group in enumerate(m.children):
                                for host_group_name in host.group_names:
                                    if group.name == host_group_name:
                                        if inventory.manufacturers[i].children[o].hosts is None:
                                            inventory.manufacturers[i].children[o].hosts = []
                                        inventory.manufacturers[i].children[o].hosts.append(host)

    @staticmethod
    def modify_host(original_host: Host, modified_host: Host, send_remove: bool = True, send_add: bool = True):
        DaoHost.remove_host(original_host, send=send_remove)
        DaoHost.add_host(modified_host, send=send_add)

    @staticmethod
    def remove_host(host: Host, send: bool = True) -> None:
        with Inventory().readwrite(send=send) as inventory:
            for i, m in enumerate(inventory.manufacturers):
                if m.name == host.manufacturer_name:
                    if m.hosts:
                        if host in m.hosts:
                            inventory.manufacturers[i].hosts.remove(host)
                if m.children:
                    for o, group in enumerate(m.children):
                        for host_group_name in host.group_names:
                            if group.name == host_group_name and group.hosts:
                                try:
                                    inventory.manufacturers[i].children[o].hosts.remove(host)
                                except (ValueError, AttributeError):
                                    pass
