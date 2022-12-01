from rich.panel import Panel

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_variables.cli_variable_input import CLIVariableInput
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.configuration.dao.dao_variable import DaoVariable


class MenuVariableNew(Menu):
    def __init__(self, console):
        super().__init__(
            console=console,
            path=CLIPaths.VARIABLES_NEW.value
        )

    def start(self):
        new_variable = CLIVariableInput().get_variable_from_user(console=self.console)
        if new_variable:
            DaoVariable().add_variable(variable=new_variable)
            self.console.print(
                Panel(f"The variable {new_variable.name} has been added successfully!",
                      title="Process completed!"),
                style=str(Color.SUCCESS.value)
            )
        wait_for_user_to_continue(console=self.console)
