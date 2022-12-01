from rich.console import Console

from app.cli.cli_components.multiselection import MultiSelection
from app.cli.cli_components.user_input import UserInput
from app.cli.enum.color import Color
from app.inventory.dao import DaoHost, DaoGroup
from app.inventory.model.host import Host


class CLIHostInputs:
    @staticmethod
    def _get_host_inform_user(console):
        console.print("Please enter the following requested information about the new host.\n"
                      "If an option does not apply to the host you want to add, just hit enter.")
        console.print("\nAddress Information", style=str(Color.HOST.value))

    @staticmethod
    def _get_host_default_values(default_host) -> tuple[str, str, str, str, str]:
        if default_host:
            return \
                f"{default_host.ipv4_address}", \
                f"{default_host.ipv6_address}", \
                f"'{default_host.fqdn}'", \
                f"'{default_host.name}'", \
                f"'{default_host.manufacturer_name}'"
        else:
            return ("",) * 5

    @staticmethod
    def reformat_information(ipv4, ipv6, fqdn, name) -> list:
        attrs = []
        for attr in (ipv4, ipv6, fqdn, name):
            attrs.append(attr.replace("'", "").replace("\"", "").replace("None", "").strip())
        return attrs

    @staticmethod
    def get_host(console, default_host=None) -> Host:
        from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_manufacturer.cli_manufacturer_inputs import \
            CLIManufacturerInputs
        from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_group.cli_group_inputs import CLIGroupInputs
        try:
            default_ipv4, default_ipv6, default_fqdn, default_name, default_manufacturer_name = \
                CLIHostInputs._get_host_default_values(default_host=default_host)

            CLIHostInputs._get_host_inform_user(console=console)
            ipv4 = UserInput(console=console, prompt="IPv4 address", default_answer=default_ipv4,
                             mandatory=False, validate_func=Host.validate_ipv4_address).answer
            ipv6 = UserInput(console=console, prompt="IPv6 address", default_answer=default_ipv6,
                             mandatory=False, validate_func=Host.validate_ipv6_address).answer
            fqdn = UserInput(console=console, prompt="Fully qualified domain name",
                             default_answer=default_fqdn, validate_func=Host.validate_fqdn, mandatory=False).answer
            if not Host.is_valid_address_information(console, ipv4, ipv6, fqdn):
                raise CLIHostInputs.InvalidAddressInformationException
            console.print("\nManufacturer", style=str(Color.HOST.value))
            try:
                manufacturer = CLIManufacturerInputs.get_manufacturer(
                    console=console,
                    prompt="Manufacturer",
                    default=default_manufacturer_name
                )
            except CLIManufacturerInputs.NoManufacturersException:
                console.print(
                    "Could not find a manufacturer. You have to add a manufacturer first before adding hosts!",
                    style=Color.FAIL.value
                )
                raise
            groups = DaoGroup.get_groups_for_node(node=manufacturer)
            console.print("\nGroups", style=str(Color.HOST.value))
            if groups:
                console.print("Please select the groups this host should be added to.")
                groups = CLIGroupInputs.choose_from_groups(console=console, groups=groups, child=default_host)
            else:
                groups = []
                console.print("No groups currently available for this manufacturer. Skipping group selection.")

            console.print("\nMiscellaneous", style=str(Color.HOST.value))
            name = UserInput(console=console, prompt="Name", default_answer=default_name,
                             mandatory=False, validate_func=Host.validate_name).answer

            ipv4, ipv6, fqdn, name = CLIHostInputs.reformat_information(ipv4, ipv6, fqdn, name)
            return Host(
                manufacturer_name=manufacturer.name,
                group_names=[group.name for group in groups],
                ipv6_address=ipv6,
                ipv4_address=ipv4,
                fqdn=fqdn,
                name=name
            )
        except RecursionError:
            console.print("To many recursions. Aborting process...")

    @staticmethod
    def choose_from_hosts(console: Console, parent=None, hosts=None):
        if not hosts:
            hosts = DaoHost().get_all_hosts()
        options = {}
        for host in hosts:
            if not options:
                index = 1
            else:
                index = max(options) + 1
            try:
                is_child_from_parent = host in parent.hosts
            except (AttributeError, TypeError):
                is_child_from_parent = -1
            options.setdefault(index, (host, host.name, is_child_from_parent))

        host_selection = MultiSelection(prompt="Host Selection", console=console)
        host_selection.register_and_show_options(
            options=options
        )
        hosts_and_selections = host_selection.start_selection()
        return_val = []
        for host, is_selected in hosts_and_selections:
            if is_selected != -1:
                return_val.append(host)
        return return_val

    class InvalidAddressInformationException(Exception):
        pass
