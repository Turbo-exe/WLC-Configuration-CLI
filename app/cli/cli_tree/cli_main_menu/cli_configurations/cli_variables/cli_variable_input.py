from app.cli.cli_components.selection import Selection
from app.cli.cli_components.user_input import UserInput
from app.cli.cli_components.yes_no import YesNo
from app.cli.enum.color import Color
from app.configuration.model.variable import Variable


class CLIVariableInput:
    @staticmethod
    def _inform_user(console):
        console.print("Please enter the following requested information about the new variable.\n")
        console.print("\nIdentification", style=str(Color.VARIABLE.value))

    @staticmethod
    def _default_values(default_variable: Variable) -> tuple[str, str, str]:
        if default_variable:
            return \
                f"{default_variable.name}", \
                f"{default_variable.description}", \
                f"'{default_variable.regex_string}'"
        else:
            return ("",) * 3

    def get_variable_from_user(self, console, default_variable: Variable = None) \
            -> Variable:
        try:
            default_name, default_description, default_regex_string = self._default_values(
                default_variable=default_variable
            )
            self._inform_user(console=console)
            name = UserInput(console=console, prompt="Name", default_answer=default_name,
                             mandatory=True, validate_func=Variable.validate_name).answer
            description = UserInput(console=console, prompt="Description", default_answer=default_description,
                                    mandatory=False, validate_func=Variable.validate_description).answer

            console.print("\nFunctionality", style=str(Color.VARIABLE.value))
            regex_string = UserInput(console=console, prompt="RegEx-Validation:",
                                     default_answer=default_regex_string, validate_func=Variable.validate_regex_string,
                                     mandatory=False).answer
            is_secret = YesNo(console=console, prompt="Input value (while execution) is secret").decision
            is_global = YesNo(console=console, prompt="Variable is global (is valid for all WLCs)").decision
            sel = Selection(prompt="When should the user enter the information for this variable?", console=console)
            sel.register_and_show_options({
                1: (False, "Before the execution"),
                2: (True, "During the execution")
            })
            ask_for_value_during_execution = sel.start_selection()
            return Variable(
                name=name.lower(),
                description=description,
                regex_string=regex_string,
                is_secret=is_secret,
                is_global=is_global,
                ask_for_value_during_execution=ask_for_value_during_execution
            )
        except RecursionError:
            console.print("To many recursions. Aborting process...")
