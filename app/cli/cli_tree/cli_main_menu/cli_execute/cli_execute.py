from rich.panel import Panel
from rich.table import Table, Column

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.cli_components.multiselection import MultiSelection
from app.cli.cli_components.selection import Selection
from app.cli.cli_components.user_input import UserInput
from app.cli.cli_components.yes_no import YesNo
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_collection.cli_collection_inputs import CLICollectionInputs
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_command.cli_command_input import CLICommandInputs
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.cli.execution.execute import Execute
from app.configuration.dao.dao_command import DaoCommand
from app.configuration.dao.dao_command_line import DaoCommandLine
from app.configuration.dao.dao_variable import DaoVariable
from app.configuration.model.collection import Collection
from app.configuration.model.command import Command
from app.configuration.model.command_line import CommandLine
from app.configuration.model.variable import Variable
from app.configuration.service.service_command_collection import ServiceCommandCollection
from app.inventory.dao import DaoManufacturer, DaoHost, DaoGroup


class MenuExecute(Menu):
    def __init__(self, console):
        super().__init__(
            console=console,
            path=CLIPaths.EXECUTION.value
        )
        self.selection = None
        self.commands = []
        self.nodes = []
        self.console = console

    def _get_and_show_commands(self, commands_and_collections: list):
        table = Table(
            Column(
                header="Step No.", width=8
            ),
            Column(
                header="Name"
            ),
            Column(
                header="Description"
            ),
            Column(
                header="Command(s)"
            )
        )
        commands = []
        for cmd_or_coll, _ in commands_and_collections:
            if isinstance(cmd_or_coll, Collection):
                commands.extend(ServiceCommandCollection().get_commands_by_collection_id(collection_id=cmd_or_coll.id))
            else:
                commands.append(cmd_or_coll)
        for i, command in enumerate(commands):
            table.add_row(
                str(i + 1),
                command.name,
                command.description,
                '\n'.join([cmd_line.command_line for cmd_line in DaoCommandLine().find_by_command_id(
                    command_id=command.id
                )])
            )
            table.add_row("")
        self.console.print(table)
        return commands

    def _show_hosts(self, hosts):
        table = Table(
            Column(
                header="Name",
            ),
            Column(
                header="IPv4 address"
            ),
            Column(
                header="IPv6 address"
            ),
            Column(
                header="FQDN"
            )
        )
        for host in hosts:
            table.add_row(
                host.name,
                host.ipv4_address,
                host.ipv6_address,
                host.fqdn
            )
        self.console.print(table)

    def get_commands_to_be_executed(self):
        self.console.print("Command Collections", style=str(Color.EXECUTE.value))
        self.console.print("Please select the command collections to be executed")
        collections = CLICollectionInputs().choose_from_collections(console=self.console)
        self.reset_screen()
        self.console.print("Commands", style=str(Color.EXECUTE.value))
        self.console.print("Please select the commands to be executed")
        all_commands = DaoCommand().find_all_commands()
        if not all_commands:
            raise Command.NotFoundException
        for collection in collections:
            commands_for_coll = ServiceCommandCollection().get_commands_by_collection_id(collection_id=collection.id)
            for command in commands_for_coll:
                try:
                    all_commands.remove(command)
                except ValueError:
                    pass
        commands = CLICommandInputs().choose_from_commands(
            console=self.console,
            numbered=False,
            commands_to_select_from=all_commands
        )
        self.reset_screen()
        self.console.print("Order", style=str(Color.EXECUTE.value))
        self.console.print("Please order the commands and collections in the way they should be executed.")
        options = {}
        index = 1
        for collection in collections:
            options.setdefault(index, (collection, collection.name + " - COLLECTION", -1))
            index += 1
        for command in commands:
            options.setdefault(index, (command, command.name + " - COMMAND", -1))
            index += 1
        commands_and_collections_selection = MultiSelection(prompt="Selection: ", console=self.console, numbered=True)
        commands_and_collections_selection.register_and_show_options(options=options)
        commands_and_collections = commands_and_collections_selection.start_selection()
        self.reset_screen()
        self.console.print("These commands will be executed", style=str(Color.EXECUTE.value))
        commands = self._get_and_show_commands(commands_and_collections=commands_and_collections)
        wait_for_user_to_continue(console=self.console, prompt="Press Enter to continue with the variable values...")
        return commands

    def get_hosts_to_be_executed(self):
        self.reset_screen()
        self.console.print("Manufacturer selection", style=str(Color.EXECUTE.value))
        manufacturers = DaoManufacturer().get_manufacturers()
        options = {}
        if manufacturers:
            for i, manufacturer in enumerate(manufacturers):
                options.setdefault(i + 1, (manufacturer, manufacturer.name))
        manufacturer_selection = Selection(prompt="Please select the manufacturer", console=self.console)
        manufacturer_selection.register_and_show_options(options)
        selected_manufacturer = manufacturer_selection.start_selection()
        manufacturer_hosts = selected_manufacturer.hosts
        hosts = []

        groups = DaoGroup().get_groups_for_node(node=selected_manufacturer)
        if groups:
            self.reset_screen()
            self.console.print("Group selection", style=str(Color.EXECUTE.value))
            options.clear()
            for i, group in enumerate(groups):
                options.setdefault(i + 1, (group, group.name, -1))
            group_selection = MultiSelection(
                prompt="Please select the groups, which hosts should be targeted",
                console=self.console
            )
            group_selection.register_and_show_options(options)
            selected_groups = group_selection.start_selection()
            for group, is_selected in selected_groups:
                if group.hosts and is_selected != -1:
                    hosts.extend(group.hosts)

        if manufacturer_hosts:
            self.reset_screen()
            self.console.print("Host selection", style=str(Color.EXECUTE.value))
            options.clear()
            for i, host in enumerate(manufacturer_hosts):
                options.setdefault(i + 1, (host, host.name, -1))
            host_selection = MultiSelection(
                prompt="Please select the hosts, which are not assigned to a group, but should be targeted anyway.",
                console=self.console
            )
            host_selection.register_and_show_options(options)
            selected_hosts = host_selection.start_selection()
            for host, is_selected in selected_hosts:
                if host and is_selected != -1:
                    hosts.append(host)
        self.reset_screen()
        if hosts:
            self.console.print("The commands (which you will select in the next step) will be executed on these WLCs:")
            self._show_hosts(hosts=hosts)
            wait_for_user_to_continue(self.console)
        return hosts

    def get_command_lines_with_variable_values(self, hosts, commands) -> dict[str: list[CommandLine]]:
        self.reset_screen()
        self.console.print("Variable Values", style=str(Color.EXECUTE.value))
        self.console.print("Please enter a value for each of these variables.")
        command_lines = []
        command_lines_for_hosts = {}
        answered_variables = {}
        for host in hosts:
            for command in commands:
                for command_line in DaoCommandLine().find_by_command_id(command_id=command.id):
                    variables = DaoVariable().get_variables_from_string(text=command_line.command_line)
                    cmd_line = command_line.command_line
                    if variables:
                        for variable in variables:
                            if variable.name not in answered_variables.keys():
                                variable_value = "{{" + variable.name.lower() + "}}"
                                if not variable.ask_for_value_during_execution and variable.is_global:
                                    variable_value = UserInput(
                                        console=self.console,
                                        prompt=f"{variable.name} (Description: {variable.description}): ",
                                        is_secret=variable.is_secret,
                                        validate_func=lambda inputted_value: Variable.validate_text_with_regex(
                                            str_to_validate=inputted_value,
                                            regex_string=variable.regex_string
                                        )
                                    ).answer
                                    answered_variables.setdefault(variable.name, variable_value)
                                elif not variable.ask_for_value_during_execution and not variable.is_global:
                                    variable_value = UserInput(
                                        console=self.console,
                                        prompt=f"{variable.name} (Description: {variable.description}) "
                                               f"-> For host '{host.name}'): ",
                                        is_secret=variable.is_secret,
                                        validate_func=lambda inputted_value: Variable.validate_text_with_regex(
                                            str_to_validate=inputted_value,
                                            regex_string=variable.regex_string
                                        )
                                    ).answer
                            else:
                                variable_value = answered_variables.get(variable.name)
                            cmd_line = cmd_line.replace(
                                "{{" + variable.name.lower() + "}}", variable_value)
                    command_lines.append(cmd_line)
            command_lines_for_hosts.setdefault(host, command_lines.copy())
            command_lines.clear()
        return command_lines_for_hosts

    def add_command_for_entering_config_mode(self, command_lines_for_host: dict[str: list[CommandLine]]):
        self.reset_screen()
        self.console.print("Configuration Mode Command", style=str(Color.EXECUTE.value))
        self.console.print("Please enter the command to get into the configuration mode on "
                           "the target hosts\n(e.g. for Cisco this would be ' configure terminal ')")
        command_for_config_mode = UserInput(console=self.console,
                                            prompt="Config entry command: ",
                                            mandatory=False).answer
        if command_for_config_mode:
            for _, command_lines in command_lines_for_host.items():
                command_lines.insert(0, command_for_config_mode)
                # command_lines_for_host.update(
                #     {
                #         host: command_lines.insert(
                #             0, CommandLine(id_=-1, command_id=-1, command_line=command_for_config_mode)
                #         )
                #     }
                # )

    def ask_to_start(self, command_lines: dict[str: list[CommandLine]]):
        self.console.print(Panel("All necessary information has been entered.\n"
                                 "The execution process can now be started!", style=str(Color.SUCCESS.value)),
                           justify="center")
        answer = YesNo(console=self.console, prompt="Do you want to start the execution process?").decision
        if answer:
            self.console.print("Execution started.")
            Execute(console=self.console, command_lines_for_host=command_lines)
            wait_for_user_to_continue(self.console, prompt="Execution finished. Please press Enter to continue...")
        else:
            self.console.print(
                Panel("Did not start the execution process",
                      title="Process cancelled!"),
                style=str(Color.FAIL.value))

    def start(self):
        self.reset_screen()
        if not DaoManufacturer().get_manufacturers():
            self.console.print(
                Panel("No manufacturers added to the system. Add manufacturers first to start configuring!",
                      title="Process aborted!"),
                style=str(Color.FAIL.value)
            )
            wait_for_user_to_continue(console=self.console)
            return
        if not DaoHost().get_all_hosts():
            self.console.print(
                Panel("No hosts added to the system. Add hosts first to start configuring!",
                      title="Process aborted!"),
                style=str(Color.FAIL.value))
            wait_for_user_to_continue(console=self.console)
            return
        hosts = self.get_hosts_to_be_executed()
        if not hosts:
            self.console.print(
                Panel("No hosts were selected. Aborting execution process...",
                      title="Process aborted!"),
                style=str(Color.FAIL.value))
            wait_for_user_to_continue(console=self.console)
            return
        try:
            commands = self.get_commands_to_be_executed()
        except Command.NotFoundException:
            self.console.print(
                Panel("No commands found to be executed. Add commands first to start configuring!",
                      title="Process aborted!"),
                style=str(Color.FAIL.value))
            wait_for_user_to_continue(console=self.console)
            return
        command_lines = self.get_command_lines_with_variable_values(hosts=hosts, commands=commands)
        self.add_command_for_entering_config_mode(command_lines_for_host=command_lines)
        self.ask_to_start(command_lines=command_lines)
