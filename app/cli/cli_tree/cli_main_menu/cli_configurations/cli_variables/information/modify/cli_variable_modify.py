from rich.console import Console
from rich.panel import Panel

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_variables.cli_variable_input import CLIVariableInput
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.configuration.dao.dao_variable import DaoVariable
from app.configuration.model.variable import Variable


class MenuVariableModify(Menu):
    def __init__(self, console: Console, variable: Variable):
        super().__init__(
            console=console,
            path=CLIPaths.VARIABLES_MODIFY.value
        )
        self.variable = variable

    def start(self):
        modified_variable = CLIVariableInput().get_variable_from_user(
            console=self.console,
            default_variable=self.variable
        )
        if modified_variable:
            DaoVariable().modify_variable(
                variable=self.variable,
                name=modified_variable.name,
                description=modified_variable.description,
                regex_string=modified_variable.regex_string,
                is_secret=modified_variable.is_secret,
                ask_for_value_during_execution=modified_variable.ask_for_value_during_execution
            )
            self.console.print(
                Panel(f"The variable {modified_variable.name} has been modified successfully!",
                      title="Process completed!"),
                style=str(Color.SUCCESS.value)
            )
        else:
            self.console.print(
                Panel(f"Something went wrong. Can't modify this variable!",
                      title="Process aborted!"),
                style=str(Color.FAIL.value)
            )
        wait_for_user_to_continue(console=self.console)
