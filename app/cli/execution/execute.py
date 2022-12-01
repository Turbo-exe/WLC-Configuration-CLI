from getpass import getpass
from time import sleep

import netmiko.exceptions
from netmiko import ConnectHandler
from rich.console import Console

from app.cli.cli_components.status import Status
from app.cli.cli_components.user_input import UserInput
from app.cli.enum.color import Color
from app.configuration.dao.dao_variable import DaoVariable
from app.configuration.model.variable import Variable
from app.inventory.model.host import Host


class Execute:
    def __init__(self, console: Console, command_lines_for_host: dict[Host: list[str]]):
        self.console = console
        self.command_lines_for_host = command_lines_for_host
        self._start_execution()
        self.status = Status()

    def _fill_out_command_line_variables(self, command_line: str):
        variables = DaoVariable().get_variables_from_string(text=command_line)
        if variables:
            self.console.print("\nPlease provide the value for the following variable(s):",
                               style=str(Color.EXECUTE.value) + " bold blink")
            for variable in variables:
                variable_value = UserInput(
                    console=self.console,
                    prompt=f"{variable.name} ({variable.description}): ",
                    is_secret=variable.is_secret,
                    validate_func=lambda inputted_value: Variable.validate_text_with_regex(
                        str_to_validate=inputted_value,
                        regex_string=variable.regex_string
                    )
                ).answer
                command_line = command_line.replace("{{" + variable.name.lower() + "}}", variable_value)
            self.console.print("\n")
        return command_line

    def _start_execution(self):
        self.status = Status()
        for host, command_lines in self.command_lines_for_host.items():
            self.status.show_status(f"Connecting to WLC '{host.name}' using address '{host.address}'")
            try:
                with ConnectHandler(host=host.address,
                                    port=22,
                                    username='',
                                    password='',
                                    device_type='cisco_wlc_ssh') as ch:
                    self._execute_command_lines(connection_handler=ch, host=host, command_lines=command_lines)

            except (netmiko.ConnectionException, netmiko.NetmikoTimeoutException):
                self.console.log(f"Connection to WLC '{host.name}' failed. Continuing to next WLC.",
                                 style=str(Color.FAIL.value))
            except netmiko.NetmikoAuthenticationException:
                self.status.stop_status()
                sleep(0.05)
                self.console.log(
                    "Destination host has authentication set up.\n"
                    f"Please provide the login information for the host {host.name} (address={host.address}).",
                    style=str(Color.EXECUTE.value)
                )
                username = input(f"Username for '{host.address}: ")
                password = getpass("Password: ")
                self.status.show_status(f"Connecting to WLC '{host.name}' using address"
                                        f" '{host.address}' and user '{username}'")
                with ConnectHandler(host=host.address,
                                    port=22,
                                    username=username,
                                    password=password,
                                    device_type='cisco_wlc_ssh') as ch:
                    self._execute_command_lines(connection_handler=ch, host=host, command_lines=command_lines)

    def _execute_command_lines(self, connection_handler, host, command_lines):
        self.status.stop_status()
        self.console.log(f"Successfully connected to WLC '{host.name}'", style=str(Color.SUCCESS.value))
        for command_line in command_lines:
            command_line = self._fill_out_command_line_variables(
                command_line=command_line
            )
            self.console.log("   Executing command: ", command_line)
            connection_handler.send_command_timing(command_string=command_line, last_read=0.5)
