from yaml import safe_dump

from app.inventory.file.read_inventory import ReadInventory


class WriteInventory(ReadInventory):
    def __raw_write_group(self, group):
        return_val = {
            "hosts": self.__raw_write_hosts(group)
        }
        if group.children is not None:
            return_val.setdefault("children", dict(self.__raw_write_groups(group)))
        return return_val

    def __raw_write_groups(self, parent):
        if parent.children:
            groups = {}
            for group in parent.children:
                groups[group.name] = self.__raw_write_group(group)
            return groups
        else:
            return None

    @staticmethod
    def __raw_write_hosts(parent):
        if parent.hosts:
            hosts = {}
            for host in parent.hosts:
                hosts[host.address] = {
                    "ipv4": host.ipv4_address,
                    "ipv6": host.ipv6_address,
                    "fqdn": host.fqdn,
                    "name": host.name,
                    "manufacturer_name": host.manufacturer_name,
                    "group_names": host.group_names
                }
            return hosts
        else:
            return None

    def __raw_write_manufacturers(self):
        manufacturers = {}
        for manufacturer in self.manufacturers:
            manufacturers[manufacturer.name] = {
                "children": self.__raw_write_groups(parent=manufacturer),
                "hosts": self.__raw_write_hosts(parent=manufacturer)
            }
        return manufacturers

    def write_inventory(self):
        raw_dict = {"all": {"children": self.__raw_write_manufacturers()}}
        raw_inventory = safe_dump(raw_dict).replace("null", "")
        with open("app/inventory/inventory.yaml", "w") as inventory_file:
            inventory_file.write(raw_inventory)
