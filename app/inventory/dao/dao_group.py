from app.inventory.dao import DaoManufacturer
from app.inventory.file.inventory import Inventory
from app.inventory.model.group import Group
from app.inventory.model.host import Host
from app.inventory.model.manufacturer import Manufacturer
from app.inventory.dao import DaoHost


class DaoGroup:
    @staticmethod
    def get_group_for_manufacturer(manufacturer: Manufacturer, group_name: str) -> Group:
        for group in manufacturer.children:
            if group_name == group.name:
                return group

    @staticmethod
    def get_groups_for_node(node: Manufacturer or Group) -> list[Group]:
        try:
            return node.children
        except AttributeError:
            return []

    @staticmethod
    def get_all_groups() -> list[Group]:
        groups = []
        for manufacturer in DaoManufacturer().get_manufacturers():
            g = DaoGroup.get_groups_for_node(node=manufacturer)
            if not g:
                g = []
            groups.extend(g)
        return groups

    @staticmethod
    def add_group_to_manufacturer(group: Group) -> None:
        with Inventory().readwrite() as inventory:
            for i, m in enumerate(inventory.manufacturers):
                if m.name == group.manufacturer_name:
                    if inventory.manufacturers[i].children is None:
                        inventory.manufacturers[i].children = []
                    inventory.manufacturers[i].children.append(group)

        if group.hosts:
            for host in group.hosts:
                manufacturer = DaoManufacturer().get_manufacturer_by_name(host.manufacturer_name)
                if manufacturer.hosts:
                    if host in manufacturer.hosts:
                        DaoHost().remove_host(host=host)
                group_names = host.group_names
                if group.name not in group_names:
                    group_names.append(group.name)
                DaoHost().add_host(
                    host=Host(
                        manufacturer_name=host.manufacturer_name,
                        ipv4_address=host.ipv4_address,
                        ipv6_address=host.ipv6_address,
                        fqdn=host.fqdn,
                        name=host.name,
                        group_names=group_names
                    )
                )

    @staticmethod
    def modify_group(original_group: Group, modified_group: Group):
        DaoGroup.remove_group_from_manufacturer(group=original_group, send=False)
        DaoGroup.add_group_to_manufacturer(modified_group)

    @staticmethod
    def remove_group_from_manufacturer(group: Group, send: bool = True):
        with Inventory().readwrite(send=send) as inventory:
            for i, m in enumerate(inventory.manufacturers):
                if m.name == group.manufacturer_name:
                    if m.children:
                        try:
                            inventory.manufacturers[i].children.remove(group)
                            if group.hosts:
                                for host in group.hosts:
                                    if not DaoHost().get_occurrences_of_host_in_node(host=host, parent=m):
                                        if not m.hosts:
                                            inventory.manufacturers[i].hosts = []
                                        host.group_names = []
                                        DaoHost().add_host(host=host)
                                        inventory.manufacturers[i].hosts.append(host)
                                    else:
                                        group_names = host.group_names.copy()
                                        group_names.remove(group.name)
                                        DaoHost().modify_host(
                                            original_host=host,
                                            modified_host=Host(
                                                manufacturer_name=host.manufacturer_name,
                                                ipv4_address=host.ipv4_address,
                                                ipv6_address=host.ipv6_address,
                                                fqdn=host.fqdn,
                                                name=host.name,
                                                group_names=group_names
                                            )
                                        )
                                        group.hosts.remove(host)
                                for host in DaoHost().get_hosts_for_node(node=m, recursive=True):
                                    if host.group_names:
                                        if group.name in host.group_names:
                                            host.group_names.remove(group.name)
                        except ValueError:
                            pass
