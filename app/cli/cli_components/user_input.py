from getpass import getpass

from rich.console import Console

from app.cli.cli_components.menu import Menu


class UserInput:
    def __init__(self, console: Console, prompt: str, default_answer: str = None, mandatory: bool = True,
                 validate_func: callable = None, is_secret: bool = False):
        self.console = console
        self.prompt = prompt.strip()
        self.prompt_with_default = self.prompt.strip()
        self.default_answer = default_answer
        self.mandatory = mandatory
        self.validate_func = validate_func
        self.is_secret = is_secret
        self._start()

    def _start(self):
        self.prompt_with_default = self._format_prompt()
        self.answer = self._get_answer_from_user()
        if self._answer_is_empty_and_default_exists():
            self.answer = self.default_answer
            self._output_users_answer()
        elif self._answer_and_default_is_empty_but_mandatory():
            self.answer = self._start()
        elif self.validate_func:
            try:
                self.validate_func(self.answer)
            except Exception as exception:
                # noinspection PyUnresolvedReferences
                Menu.clear_last_line(len_last_line=len(self.prompt_with_default) + len(str(self.answer)))
                try:
                    self.console.print(exception.message)
                except AttributeError:
                    self.console.print("Invalid input!")
                self.answer = self._start()
            else:
                self._output_users_answer()
        else:
            self._output_users_answer()
        return self.answer

    def _answer_is_empty_and_default_exists(self):
        return self.default_answer and not self.answer

    def _output_users_answer(self):
        Menu.clear_last_line(len_last_line=len(self.prompt_with_default) + len(str(self.answer)))
        if self.is_secret:
            self.console.print(f"{self.prompt}: (hidden)")
        else:
            self.console.print(f"{self.prompt}: {self.answer}")

    def _answer_and_default_is_empty_but_mandatory(self):
        return not self.default_answer and not self.answer and self.mandatory

    def _get_answer_from_user(self):
        if self.is_secret:
            return getpass(self.prompt_with_default)
        else:
            return self.console.input(self.prompt_with_default).strip()

    @staticmethod
    def _add_default_to_prompt(prompt: str, default_answer: str):
        return f"{prompt} (default={default_answer})"

    @staticmethod
    def _add_colon_to_prompt(prompt: str):
        if not prompt.strip().endswith(":"):
            prompt += ": "
        return prompt

    def _format_prompt(self):
        prompt = self.prompt
        if self.default_answer:
            prompt = UserInput._add_default_to_prompt(prompt=self.prompt, default_answer=self.default_answer)
        prompt = UserInput._add_colon_to_prompt(prompt=prompt)
        return prompt.strip() + " "
