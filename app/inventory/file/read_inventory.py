from yaml import safe_load

from app.inventory.model.group import Group
from app.inventory.model.host import Host
from app.inventory.model.inv import Inv
from app.inventory.model.manufacturer import Manufacturer


class ReadInventory(Inv):
    def read_inventory(self):
        raw_data = self._read_raw_inventory()
        self.manufacturers = self._build_inventory(raw_data=raw_data)
        return self.manufacturers

    @staticmethod
    def _read_raw_inventory():
        with open("app/inventory/inventory.yaml", "r") as inventory_file:
            return safe_load(inventory_file)

    @staticmethod
    def _raw_inv_has_hosts(raw_inv_data):
        try:
            _ = raw_inv_data["hosts"]
            return True
        except (TypeError, KeyError):
            return False

    @staticmethod
    def _raw_inv_has_groups(raw_inv_data):
        try:
            _ = raw_inv_data["children"]
            return True
        except (TypeError, KeyError):
            return False

    @staticmethod
    def _raw_in_get_group_names_for_host(group_names: str) -> list[str]:
        if not group_names:
            return []
        group_names = group_names.split(", ")
        for group_name in group_names:
            if not len(group_name):
                group_names.remove(group_name)

        if len(group_names):
            return group_names
        else:
            return []

    def _raw_inv_get_hosts(self, raw_inv_data: dict):
        hosts = []
        if self._raw_inv_has_hosts(raw_inv_data):
            raw_hosts = raw_inv_data["hosts"]
            if raw_hosts:
                for _, raw_host in raw_hosts.items():
                    ipv4 = raw_host["ipv4"]
                    ipv6 = raw_host["ipv6"]
                    fqdn = raw_host["fqdn"]
                    name = raw_host["name"]
                    manufacturer_name = raw_host["manufacturer_name"]
                    group_names = raw_host["group_names"]
                    hosts.append(
                        Host(
                            ipv4_address=ipv4,
                            ipv6_address=ipv6,
                            fqdn=fqdn,
                            name=name,
                            manufacturer_name=manufacturer_name,
                            group_names=group_names)
                    )
        if hosts:
            return hosts
        else:
            return

    def _raw_inv_get_groups(self, raw_parent: dict, manufacturer: str):
        if not self._raw_inv_has_groups(raw_parent):
            return
        groups = []
        raw_groups = raw_parent["children"]
        if raw_groups:
            for group, data in raw_groups.items():
                hosts = self._raw_inv_get_hosts(data)
                sub_children = self._raw_inv_get_groups(data, manufacturer=manufacturer)
                groups.append(
                    Group(
                        name=group,
                        manufacturer_name=manufacturer,
                        hosts=hosts,
                        children=sub_children
                    )
                )
            return groups
        else:
            return None

    def _build_inventory(self, raw_data):
        manufacturers = []
        try:
            for manufacturer, data in raw_data["all"]["children"].items():
                hosts = self._raw_inv_get_hosts(raw_inv_data=data)
                groups = self._raw_inv_get_groups(raw_parent=data, manufacturer=manufacturer)
                manufacturers.append(
                    Manufacturer(
                        name=manufacturer,
                        hosts=hosts,
                        children=groups
                    )
                )
        except (TypeError, AttributeError):
            raise
        return manufacturers
