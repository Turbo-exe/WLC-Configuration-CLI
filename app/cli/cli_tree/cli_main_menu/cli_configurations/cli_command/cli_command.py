from app.cli.cli_components.menu import Menu
from app.cli.cli_components.selection import Selection
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_command.information.cli_command_information import \
    MenuCommandInformation
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_command.new.cli_command_new import \
    MenuCommandNew
from app.cli.enum.cli_options import CLIPaths
from app.configuration.dao.dao_command import DaoCommand
from app.configuration.model.command import Command


class MenuCommand(Menu):
    def __init__(self, console, prompt: str = "Please select one of these commands"):
        super().__init__(
            console=console,
            path=CLIPaths.COMMANDS.value
        )
        self.selection = None
        self.console = console
        self.selection_command = None
        self.commands = {}
        self.commands.clear()
        self.prompt = prompt

    def _load_options(self):
        commands = DaoCommand().find_all_commands()
        if commands:
            for command in commands:
                self._add_command_selection(command=command)
        self._add_new_option()
        self._add_back_option()

    def _add_back_option(self):
        if self.commands:
            if max(self.commands) < 99:
                index = 99
            else:
                index = max(self.commands) + 1
        else:
            index = 99
        self.commands.setdefault(index, (CLIPaths.BACK, "value"))

    def _add_new_option(self):
        if self.commands:
            index = max(self.commands) + 1
        else:
            index = 1
        self.commands.setdefault(index, (MenuCommandNew(console=self.console), "name"))

    def _add_command_selection(self, command: Command) -> int:
        index = 1
        if self.commands:
            index = max(self.commands) + 1
        self.commands.setdefault(
            index,
            (MenuCommandInformation(console=self.console, command=command), command.name)
        )
        return index

    def _setup_command_selection(self):
        self.selection_command = Selection(prompt=self.prompt, console=self.console)
        self.selection_command.register_and_show_options(self.commands)

    def start(self):
        self.reset_screen()
        self._load_options()
        self._setup_command_selection()
        selection = self.selection_command.start_selection()
        self.horizontal_spacer()
        self._decide_upon_selection(selected_option=selection)

    def _decide_upon_selection(self, selected_option):
        self.commands.clear()
        super()._decide_upon_selection(selected_option=selected_option)
