from app.inventory.file.inventory import Inventory
from app.inventory.model.manufacturer import Manufacturer


class DaoManufacturer:
    @staticmethod
    def get_manufacturers() -> list[Manufacturer]:
        with Inventory().read() as inventory:
            manufacturers = inventory.manufacturers
        return manufacturers

    @staticmethod
    def get_manufacturer_by_name(manufacturer_name: str) -> Manufacturer:
        with Inventory().read() as inventory:
            for manufacturer in inventory.manufacturers:
                if manufacturer_name.upper() == manufacturer.name:
                    return manufacturer

    def add_manufacturer(self, manufacturer_name: str) -> None:
        if Manufacturer.validate_name(name=manufacturer_name):
            raise Manufacturer.ManufacturerNameInvalidException
        if self.manufacturer_name_already_exists(name=manufacturer_name):
            raise Manufacturer.ManufacturerExistsException
        with Inventory().readwrite() as inventory:
            inventory.manufacturers.append(
                Manufacturer(
                    name=manufacturer_name
                )
            )

    def rename_manufacturer(self, manufacturer: Manufacturer, new_name: str) -> None:
        if Manufacturer.validate_name(name=new_name):
            raise Manufacturer.ManufacturerNameInvalidException
        if self.manufacturer_name_already_exists(name=new_name):
            raise Manufacturer.ManufacturerExistsException
        with Inventory().readwrite() as inventory:
            for i, m in enumerate(inventory.manufacturers):
                if m == manufacturer:
                    inventory.manufacturers[i].name = new_name
                    break

    @staticmethod
    def delete_manufacturer(manufacturer: Manufacturer) -> None:
        with Inventory().readwrite() as inventory:
            for i, m in enumerate(inventory.manufacturers):
                if m.name == manufacturer.name:
                    inventory.manufacturers.pop(i)
                    break

    def manufacturer_name_already_exists(self, name: str) -> bool:
        return self.get_manufacturer_by_name(manufacturer_name=name) is not None

    #
    # def write_new_manufacturer(self, name):
    #     with open(self.inventory_file, "a") as inventory_file:
    #         inventory_file.write(f"\n[{name}]")
    #
    # def get_manufacturers(self) -> list[str]:
    #     manufacturers = []
    #     with open(self.inventory_file, "r") as inventory_file:
    #         for line in inventory_file.readlines():
    #             if self.line_is_manufacturer(line=line):
    #                 manufacturers.append(self.get_manufacturer_name_from_line(line=line))
    #     manufacturers = self.remove_duplicate_manufacturers(list_of_manufacturers=manufacturers)
    #     return manufacturers
    #
    # def get_manufacturers_with_indices(self) -> list[tuple[int, str]]:
    #     manufacturers = []
    #     with open(self.inventory_file, "r") as inventory_file:
    #         for i, line in enumerate(inventory_file.readlines()):
    #             if self.line_is_manufacturer(line=line):
    #                 manufacturers.append((i, self.get_manufacturer_name_from_line(line=line)))
    #     return manufacturers
    #
    # @staticmethod
    # def remove_duplicate_manufacturers(list_of_manufacturers: list) -> list:
    #     return [cli_manufacturer for i, cli_manufacturer in enumerate(list_of_manufacturers)
    #             if cli_manufacturer not in list_of_manufacturers[:i]]
    #
    # def rename_manufacturer(self, old_name, new_name):
    #     with open(self.inventory_file, "r") as inventory_file:
    #         lines = inventory_file.readlines()
    #         for i, line in enumerate(lines):
    #             line = line.replace(old_name.upper(), new_name.upper())
    #             lines[i] = line
    #     with open(self.inventory_file, "w") as inventory_file:
    #         inventory_file.writelines(lines)
    #
    # def delete_manufacturer(self, name: str):
    #     with open("inventory.yaml", "r") as inventory_file:
    #         original_lines = inventory_file.readlines()
    #         manufacturer_occurrences = 0
    #         for line in original_lines:
    #             if name in line:
    #                 manufacturer_occurrences += 1
    #
    #         for _ in range(manufacturer_occurrences):
    #             lines = original_lines
    #             for line in lines:
    #                 if name in line:
    #                     start_index = lines.index(line)
    #                     break
    #             lines = lines[start_index:]
    #             start_line = lines.pop(0)
    #             for line in lines:
    #                 if line.find("[") != -1 or line.find("]") != -1:
    #                     end_index = lines.index(line) + 1
    #                     break
    #             else:
    #                 end_index = len(original_lines)
    #             lines.insert(0, start_line)
    #             original_lines = original_lines[0: start_index] + original_lines[start_index+end_index:]
    #     with open("inventory.yaml", "w") as inventory_file:
    #         inventory_file.writelines(original_lines)
    #
    # def is_valid_manufacturer_name(self, console, name):
    #     if self.name_contains_illegal_chars(name=name):
    #         console.print(Panel("This name is invalid. It must not contain '___' or a number on the start!",
    #                             title="Process aborted!"),
    #                       style="red")
    #         return False
    #     if self.manufacturer_name_already_exists(name=name):
    #         console.print(Panel("This cli_manufacturer name is already in use! The process will be aborted.",
    #                             title="Process aborted!"),
    #                       style="red")
    #         return False
    #     return True
    #
    # def manufacturer_name_already_exists(self, name):
    #     manufacturers = self.get_manufacturers()
    #     return name in manufacturers
    #
    # @staticmethod
    # def line_is_manufacturer(line: str) -> bool:
    #     line = line.strip()
    #     return line.find("[") != -1 or line.find("]") != -1
    #
    # @staticmethod
    # def line_is_specific_manufacturer(line: str, cli_manufacturer: str) -> bool:
    #     line = line.strip()
    #     return line.find(cli_manufacturer) != -1 and (line.find("[") != -1 or line.find("]") != -1)
    #
    # def get_manufacturer_name_from_line(self, line: str) -> str:
    #     line = line.strip()
    #     name = self.remove_brackets_from_line(line=line)
    #     return self.remove_groups_from_manufacturer_name(name=name)
    #
    # @staticmethod
    # def remove_brackets_from_line(line: str) -> str:
    #     for char in ["[", "]"]:
    #         line = line.replace(char, "")
    #     return line
    #
    # @staticmethod
    # def remove_groups_from_manufacturer_name(name: str) -> str:
    #     parts = name.split("___")
    #     return parts[0]
    #
    # @staticmethod
    # def name_contains_illegal_chars(name: str) -> bool:
    #     if len(name) == 0:
    #         return True
    #     if name.find("___") != -1:
    #         return True
    #     try:
    #         int(name[0])
    #         return True
    #     except ValueError:
    #         pass
    #     return False
