from sys import stdin

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel

from app.cli.cli_components.menu import Menu
from app.cli.cli_components.multiselection import MultiSelection
from app.cli.cli_components.user_input import UserInput
from app.cli.enum.color import Color
from app.configuration.dao.dao_command import DaoCommand
from app.configuration.dao.dao_command_collection import DaoCommandCollection
from app.configuration.dao.dao_command_line import DaoCommandLine
from app.configuration.dao.dao_variable import DaoVariable
from app.configuration.model.command import Command
from app.configuration.model.command_collection import CommandCollection
from app.configuration.model.command_line import CommandLine


class CLICommandInputs:
    @staticmethod
    def _inform_user(console):
        console.print("Please enter the following requested information about the new command.\n")
        console.print("\nIdentification", style=str(Color.COMMAND.value))

    @staticmethod
    def _default_values(default_command) -> tuple[str, str]:
        if default_command:
            return \
                f"{default_command.name}", \
                f"{default_command.description}"
        else:
            return ("",) * 2

    def get_command_from_user(self, console: Console, default_command: Command = None) \
            -> tuple[Command, list[CommandLine]]:
        try:
            default_name, default_description = self._default_values(
                default_command=default_command
            )
            self._inform_user(console=console)
            name = UserInput(console=console, prompt="Name", default_answer=default_name,
                             mandatory=True, validate_func=Command.validate_name).answer
            description = UserInput(console=console, prompt="Description", default_answer=default_description,
                                    mandatory=False, validate_func=Command.validate_description).answer
            if default_command:
                command = DaoCommand().modify_command(
                    command=default_command,
                    id_=default_command.id,
                    name=name,
                    description=description
                )
            else:
                command = Command(
                    name=name,
                    description=description
                )

            variables = DaoVariable().find_all_variables()
            console.print("\nFunctionality", style=str(Color.COMMAND.value))
            console.print("You can now enter the command to be executed.")
            console.print("The command may contain more than one line.\n")
            console.print("Note: To use previously declared variables, write the variable name in curly brackets.")
            console.print("You may use these variables:")

            columns = Columns(
                ["  {{" + variable.name + "}}  " for variable in variables]
            )
            console.print(Panel(columns))
            console.print("Your Command:", style=str(Color.COMMAND.value))
            command_lines = []
            if default_command:
                default_command_lines = DaoCommandLine().find_by_command_id(command_id=default_command.id)
            else:
                default_command_lines = []
            counter = 1
            while counter:
                default_val = None
                if default_command_lines:
                    if counter <= len(default_command_lines):
                        default_val = default_command_lines[counter-1].command_line
                        prompt = f"Line {counter} (default: {default_val}): "
                    else:
                        prompt = f"Line {counter}: "
                else:
                    prompt = f"Line {counter}: "
                command_line = console.input(prompt=prompt)
                if DaoVariable().string_contains_variable(text=command_line):
                    Menu.clear_last_line(len_last_line=len(prompt + command_line))
                    command_line = DaoVariable().reformat_variables_in_string(text=command_line)
                    console.print(f"Line {counter}: {command_line}")
                if not command_line:
                    if default_val:
                        Menu.clear_last_line(len_last_line=len(prompt))
                        console.print(f"Line {counter}: {default_val}")
                        command_line = default_val
                    else:
                        break
                if default_command_lines:
                    for default_command_line in default_command_lines:
                        if default_command_line.id == counter:
                            command_lines.insert(
                                counter-1,
                                DaoCommandLine().modify_command_line(
                                    command_line=default_command_line,
                                    id_=default_command_line.id,
                                    command_id=default_command_line.command_id,
                                    command_line_=command_line.strip()
                                )
                            )
                            break
                    else:
                        command_lines.append(
                            CommandLine(
                                id_=counter,
                                command_id=command.id,
                                command_line=command_line.rstrip()
                            )
                        )
                else:
                    command_lines.append(
                        CommandLine(
                            id_=counter,
                            command_id=command.id,
                            command_line=command_line.rstrip()
                        )
                    )
                counter += 1
            return command, command_lines

        except RecursionError:
            console.print("To many recursions. Aborting process...")

    @staticmethod
    def choose_from_commands(console: Console, commands_to_select_from: list[Command] = None,
                             default_commands: list[Command] = None,
                             collection_id: int = None, numbered=True) -> list:
        options = {}
        if not commands_to_select_from:
            commands_to_select_from = DaoCommand().find_all_commands()
        for command in commands_to_select_from:
            try:
                command_collection = DaoCommandCollection().find_by_command_id_and_collection_id(
                    command_id=command.id,
                    collection_id=collection_id
                )
                if command in default_commands:
                    selected = command_collection.index + 1
                else:
                    selected = -1
            except CommandCollection.NotFoundException:
                selected = -1
            if not options:
                index = 1
            else:
                index = max(options) + 1
            options.setdefault(index, (command, command.name, selected))
        if options:
            command_selection = MultiSelection(prompt="Command Selection", console=console, numbered=numbered)
            command_selection.register_and_show_options(
                options=options
            )
            commands_and_selections = command_selection.start_selection()
            return_val = []
            for command, is_selected in commands_and_selections:
                if is_selected != -1:
                    return_val.append(command)
            return return_val
        else:
            console.print("No commands found. Skipping commands selection...")
            return []
