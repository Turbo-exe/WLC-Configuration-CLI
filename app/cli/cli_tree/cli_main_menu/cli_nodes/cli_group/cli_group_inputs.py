from rich.console import Console

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.multiselection import MultiSelection
from app.cli.cli_components.user_input import UserInput
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_host.cli_host_inputs import CLIHostInputs
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_manufacturer.cli_manufacturer_inputs import CLIManufacturerInputs
from app.cli.enum.color import Color
from app.inventory.dao import DaoHost
from app.inventory.model.group import Group


class CLIGroupInputs:
    @staticmethod
    def reformat_name(name) -> str:
        return name.replace("'", "").replace("\"", "").replace("None", "").strip()

    @staticmethod
    def _get_group_inform_user(console):
        console.print("Please provide the requested information to add a new group.")
        console.print("\nName (Unique)", style=str(Color.GROUP.value))

    @staticmethod
    def get_group(console, default_group=None) -> Group:
        try:
            if default_group:
                default_name = default_group.name
                default_manufacturer_name = default_group.manufacturer_name
            else:
                default_name = None
                default_manufacturer_name = None
            CLIGroupInputs._get_group_inform_user(console=console)
            name = UserInput(console=console, prompt="Name", default_answer=default_name,
                             mandatory=True, validate_func=Group.validate_name).answer
            name = CLIGroupInputs.reformat_name(name=name)

            console.print("\nManufacturer", style=str(Color.GROUP.value))
            try:
                manufacturer = CLIManufacturerInputs.get_manufacturer(
                    console=console,
                    prompt="Manufacturer (only hosts of this type will be addable to this group)",
                    default=default_manufacturer_name
                )
            except CLIManufacturerInputs.NoManufacturersException:
                console.print(
                    "Could not find a manufacturer. You need to add a manufacturer first, before you can add groups!"
                    , style=Color.FAIL.value
                )
                raise
            console.print("\nHosts", style=str(Color.GROUP.value))
            hosts_to_choose_from = DaoHost().get_hosts_for_node(
                node=manufacturer,
                recursive=True
            )
            hosts = None
            if hosts_to_choose_from:
                hosts = CLIHostInputs.choose_from_hosts(console=console, parent=default_group,
                                                        hosts=hosts_to_choose_from)
            else:
                console.print("No hosts registered for this manufacturer. Skipping host selection.")
            return Group(
                name=name,
                manufacturer_name=manufacturer.name,
                children=None,
                hosts=hosts
            )
        except RecursionError:
            console.print("To many recursions. Aborting process...")

    @staticmethod
    def choose_from_groups(console: Console, groups: list[Group], child=None) -> list[Group]:
        options = {}
        groups = groups if groups else []
        for group in groups:
            if not options:
                index = 1
            else:
                index = max(options) + 1
            try:
                is_parent_form_child = -1 if (group.name in child.group_names) is False else 1
            except AttributeError:
                is_parent_form_child = -1
            options.setdefault(index, (group, group.name, is_parent_form_child))
        if not options:
            raise CLIGroupInputs.NoGroupsException
        group_selection = MultiSelection(prompt="Group Selection", console=console)
        group_selection.register_and_show_options(
            options=options
        )
        groups_and_selections = group_selection.start_selection()
        return_val = []
        for group, is_selected in groups_and_selections:
            if is_selected != -1:
                return_val.append(group)
        return return_val

    class InvalidName(Exception):
        def __init__(self, message):
            self.message = message

    class NoGroupsException(Exception):
        pass
