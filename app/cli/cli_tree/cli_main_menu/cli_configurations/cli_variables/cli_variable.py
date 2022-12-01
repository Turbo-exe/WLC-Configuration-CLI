from app.cli.cli_components.menu import Menu
from app.cli.cli_components.selection import Selection
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_variables.information.cli_variable_information import \
    MenuVariableInformation
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_variables.new.cli_variable_new import MenuVariableNew
from app.cli.enum.cli_options import CLIPaths
from app.configuration.dao.dao_variable import DaoVariable
from app.configuration.model.variable import Variable


class MenuVariable(Menu):
    def __init__(self, console, prompt: str = "Please select one of these variables"):
        super().__init__(
            console=console,
            path=CLIPaths.VARIABLES.value
        )
        self.selection = None
        self.console = console
        self.selection_variable = None
        self.variables = {}
        self.variables.clear()
        self.prompt = prompt

    def _load_options(self):
        variables = DaoVariable().find_all_variables()
        if variables:
            for var in variables:
                self._add_variable_to_selection(variable=var)
        self._add_new_option()
        self._add_back_option()

    def _add_back_option(self):
        if self.variables:
            if max(self.variables) < 99:
                index = 99
            else:
                index = max(self.variables) + 1
        else:
            index = 99
        self.variables.setdefault(index, (CLIPaths.BACK, "value"))

    def _add_new_option(self):
        if self.variables:
            index = max(self.variables) + 1
        else:
            index = 1
        self.variables.setdefault(index, (MenuVariableNew(console=self.console), "name"))

    def _add_variable_to_selection(self, variable: Variable) -> int:
        index = 1
        if self.variables:
            index = max(self.variables) + 1
        self.variables.setdefault(
            index,
            (MenuVariableInformation(console=self.console, variable=variable), variable.name)
        )
        return index

    def _setup_variable_selection(self):
        self.selection_variable = Selection(prompt=self.prompt, console=self.console)
        self.selection_variable.register_and_show_options(self.variables)

    def start(self):
        self.reset_screen()
        self._load_options()
        self._setup_variable_selection()
        selection = self.selection_variable.start_selection()
        self.horizontal_spacer()
        self._decide_upon_selection(selected_option=selection)

    def _decide_upon_selection(self, selected_option):
        self.variables.clear()
        super()._decide_upon_selection(selected_option=selected_option)
