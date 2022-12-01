from rich.columns import Columns
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.inventory.dao import DaoManufacturer, DaoGroup
from app.inventory.model.group import Group
from app.inventory.model.host import Host
from app.inventory.model.manufacturer import Manufacturer


class MenuOverview(Menu):
    def __init__(self, console, nodes: list[Host or Group or Manufacturer] = None):
        super().__init__(
            console=console,
            path=CLIPaths.OVERVIEW.value
        )
        self.nodes = nodes if nodes else []
        self.all_nodes = self._get_valid_nodes()
        # self.manufacturers = self._get_valid_manufacturers()
        # self.groups = self._get_valid_groups()
        self.manufacturer_trees = self._load_tree()
        self.legend = self._load_legend()

    def _get_valid_nodes(self) -> list:
        valid_nodes = []
        for node in self.nodes:
            valid_nodes.append(node)
            valid_nodes.extend(self._get_valid_nodes_downstream(parent=node))
            valid_nodes.extend(self._get_valid_nodes_upstream(child=node))
        return valid_nodes

    def _get_valid_nodes_downstream(self, parent) -> list:
        valid_nodes = []
        if parent:
            try:
                children = parent.children
                if children:
                    for child in children:
                        valid_nodes.append(child)
                        valid_nodes.extend(self._get_valid_nodes_downstream(parent=child))
            except AttributeError:
                pass
            try:
                hosts = parent.hosts
                if hosts:
                    valid_nodes.extend(hosts)
            except AttributeError:
                pass
        return valid_nodes

    @staticmethod
    def _get_valid_nodes_upstream(child) -> list:
        valid_nodes = []
        if isinstance(child, Host):
            manufacturer = DaoManufacturer.get_manufacturer_by_name(manufacturer_name=child.manufacturer_name)
            valid_nodes.append(manufacturer)
            for group_name in child.group_names:
                group = DaoGroup.get_group_for_manufacturer(manufacturer=manufacturer, group_name=group_name)
                if group:
                    valid_nodes.append(group)
            return valid_nodes
        elif isinstance(child, Group):
            manufacturer = DaoManufacturer.get_manufacturer_by_name(manufacturer_name=child.manufacturer_name)
            valid_nodes.append(manufacturer)
            return valid_nodes
        elif isinstance(child, Manufacturer):
            return []
            # for group in

    def _get_valid_manufacturers(self) -> list[Manufacturer]:
        valid_manufacturers = []
        for node in self.nodes:
            if isinstance(node, Host) or isinstance(node, Group):
                valid_manufacturers.append(DaoManufacturer.get_manufacturer_by_name(node.manufacturer_name))
            elif isinstance(node, Manufacturer):
                valid_manufacturers.append(node)
        return valid_manufacturers

    def _get_valid_groups(self) -> list[Group]:
        valid_groups = []
        for node in self.nodes:
            if isinstance(node, Host):
                for group in DaoGroup.get_groups_for_node(
                        node=DaoManufacturer.get_manufacturer_by_name(node.manufacturer_name)):
                    if group.name in node.group_names:
                        valid_groups.append(group)
            elif isinstance(node, Group):
                valid_groups.append(node)
        return valid_groups

    def _get_style_for_node(self, node):
        if node in self.nodes:
            return "blink bold"
        else:
            return ""

    def _load_hosts(self, parent_node_of_hosts, upper_tree_branch):
        if parent_node_of_hosts.hosts:
            for host in parent_node_of_hosts.hosts:
                upper_tree_branch.add(
                    f"[{Color.HOST.value}]{host.name}",
                    style=self._get_style_for_node(node=host)
                )

    def _load_groups(self, parent_node_of_groups, upper_tree_branch):
        if parent_node_of_groups.children:
            for group in parent_node_of_groups.children:
                if group in self.all_nodes or not self.nodes:
                    tree_group = upper_tree_branch.add(
                        f"[{Color.GROUP.value}]{group.name}",
                        style=self._get_style_for_node(node=group)
                    )
                    self._load_groups(
                        parent_node_of_groups=group,
                        upper_tree_branch=tree_group
                    )
                    self._load_hosts(
                        parent_node_of_hosts=group,
                        upper_tree_branch=tree_group
                    )

    def _load_tree(self) -> list[Tree]:
        manufacturer_trees = []
        for manufacturer in DaoManufacturer().get_manufacturers():
            if manufacturer in self.all_nodes or not self.nodes:
                tree_manufacturer = Tree(
                    f"[{Color.MANUFACTURER.value}]{manufacturer.name}",
                    style=self._get_style_for_node(node=manufacturer)
                )
                self._load_groups(
                    parent_node_of_groups=manufacturer,
                    upper_tree_branch=tree_manufacturer
                )
                self._load_hosts(
                    parent_node_of_hosts=manufacturer,
                    upper_tree_branch=tree_manufacturer
                )
                manufacturer_trees.append(tree_manufacturer)
        return manufacturer_trees

    @staticmethod
    def _load_legend() -> Columns:
        return Columns(
            (
                Panel(
                    Text.assemble(
                        "Color Legend\n\n",
                        ("This color ", str(Color.MANUFACTURER.value)),
                        "represents a ", ("Manufacturer\n", str(Color.MANUFACTURER.value)),
                        ("This color ", str(Color.GROUP.value)),
                        "represents a ", ("Group\n", str(Color.GROUP.value)),
                        ("This color ", str(Color.HOST.value)),
                        "represents a ", ("Host\n", str(Color.HOST.value)),
                    )
                ),
            )
        )

    def get_legend_and_tree(self) -> tuple[Columns, list[Tree]]:
        self._load_tree()
        return self.legend, self.manufacturer_trees

    def _show_tree(self):
        self.console.print(Columns(self.manufacturer_trees, padding=5, equal=True))
        self.console.print("\n")
        self.legend = self._load_legend()
        self.console.print(self.legend)

    def start(self):
        self.reset_screen()
        self._show_tree()
        wait_for_user_to_continue(console=self.console)
