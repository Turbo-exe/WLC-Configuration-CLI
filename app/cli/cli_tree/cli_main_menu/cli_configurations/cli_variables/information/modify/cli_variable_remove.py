from rich.console import Console
from rich.panel import Panel

from app.cli.cli_components.continue_conformation import wait_for_user_to_continue
from app.cli.cli_components.menu import Menu
from app.cli.cli_components.yes_no import YesNo
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color
from app.configuration.dao.dao_variable import DaoVariable
from app.configuration.model.variable import Variable


class MenuVariableRemove(Menu):
    def __init__(self, console: Console, variable: Variable):
        super().__init__(
            console=console,
            path=CLIPaths.VARIABLES_REMOVE.value
        )
        self.variable = variable

    def start(self):
        if YesNo(console=self.console,
                 prompt=f"Are you sure that you want to delete the variable '{self.variable.name}'?"
                        " This cannot be undone!").decision:

            DaoVariable().delete_variable(
                variable=self.variable
            )

            self.console.print(
                Panel(f"The variable '{self.variable.name}' has been deleted successfully!",
                      title="Process completed!"),
                style=str(Color.SUCCESS.value)
            )
        else:
            self.console.print(
                Panel(f"The process has been aborted!",
                      title="Process aborted!"),
                style=str(Color.FAIL.value)
            )
        wait_for_user_to_continue(console=self.console)
