from rich.panel import Panel
from rich.text import Text

from string import ascii_lowercase

from app.cli.cli_components.menu import Menu
from app.cli.cli_components.selection import Selection, SelectionOption
from app.cli.enum.color import Color


class MultiSelectionOption(SelectionOption):
    def __init__(self, return_value: any, text_property: str or list, index: int, selected: int) -> None:
        super().__init__(
            return_value=return_value,
            text_property=text_property,
            index=index,
        )
        self.selected = selected

    def to_selection_option(self) -> SelectionOption:
        return SelectionOption(
            return_value=self.return_value,
            text_property=self.text_property,
            index=self.index
        )

    def to_multi_selection_option(self, selection_option: SelectionOption):
        return MultiSelectionOption(
            return_value=selection_option.return_value,
            text_property=selection_option.text_property,
            index=selection_option.index,
            selected=self.selected
        )

    def select(self, max_index):
        self.selected = max_index + 1

    def deselect(self):
        self.selected = -1

    def toggle(self, max_index):
        self.selected = -1 if self.selected != -1 else max_index + 1

    def __lt__(self, other):
        if self.selected == -1:
            return False
        if other.selected == -1:
            return True
        return self.selected < other.selected

    selected: int


class MultiSelection(Selection):
    def __init__(self, prompt, console, numbered=False):
        super().__init__(prompt=prompt, console=console)
        self.console.print(Panel(Text().assemble(
            "You are able to select", (" multiple ", str(Color.SELECTION_INDEX.value)), "of the following options.\n"
            "Just type the number or the name of the option you want to select and hit ",
            ("enter", str(Color.SELECTION_INDEX.value)), ".",
            "\n",
            "\n",
            ("Special commands\n", str(Color.SELECTION_INDEX.value)),
            "Select all options:  '", ("all", str(Color.SELECTION_INDEX.value)),
            "'\nDeselect all options:  '", ("none", str(Color.SELECTION_INDEX.value)),
            "'\nEnd this selection:  '",
            ("finish", str(Color.SELECTION_INDEX.value)), "' or '",
            ("end", str(Color.SELECTION_INDEX.value)), "' or '",
            ("continue", str(Color.SELECTION_INDEX.value)), "' or '",
            ("proceed", str(Color.SELECTION_INDEX.value)), "'"
        )))
        self.len_max_text = 0
        self.numbered = numbered
        self.DELIMITERS = [",", ";", " ", "-", ".", "_", "|", "/", "\\"]

    def _show_option(self, option: MultiSelectionOption):
        if self.numbered:
            text = Text(
                f" (No. {option.selected}) " if option.selected != -1 else "   ",
                style=str(Color.SELECTION_INDEX.value) + " italic"
            )
        else:
            text = Text(" x " if option.selected != -1 else "   ", style=str(Color.SELECTION_INDEX.value))
        self.console.print(text, end="")
        self._update_max_text_length(option=option)
        super()._show_option(option=option.to_selection_option())

    def _update_max_text_length(self, option):
        self.len_max_text = max(len(option.text) + 8, self.len_max_text)

    def _register_option(self, option: MultiSelectionOption):
        if not option.index:
            index = 1
            if self.options:
                index = max(self.options) + 1
            option.index = index
        self.options.append(option)
        return option.index

    def register_and_show_options(self, options: dict[int: list[any, any, bool]]) -> None:
        for option_key, option_values in options.items():
            option = MultiSelectionOption(
                index=option_key,
                text_property=option_values[1],
                return_value=option_values[0],
                selected=option_values[2]
            )
            self._register_option(option=option)
        self._show_options()

    def _longest_line(self, prompt_including_answer: str):
        return max(self.len_max_text + self.len_max_index, len(prompt_including_answer))

    def _split_input_to_options(self, input_val: str):
        options = []
        for delimiter in self.DELIMITERS:
            if (_ := input_val.split(delimiter)) and input_val.find(delimiter) != -1:
                for option in _:
                    if option not in options and option:
                        options.append(option)
                break
        if not options:
            options.append(input_val)
        return options

    def start_selection(self, allow_empty_selection=False, _prompt="Selection: ") -> list[any, int]:
        try:
            input_val = input(_prompt)
            if input_val.lower() == "none":
                for option in self.options:
                    option.deselect()
            if input_val.lower() == "all":
                for i, option in enumerate(self.options):
                    option.select(i)
            if input_val.lower() == "finish" or input_val.lower() == "end" or \
                    input_val.lower() == "continue" or input_val.lower() == "proceed":
                Menu.clear_last_line(self._longest_line(prompt_including_answer=_prompt + input_val) + 6)
                return [(option.return_value, option.selected) for option in self.options]

            formatted_input_vals = self._split_input_to_options(input_val=input_val)
            invalid_input_vals = []
            for formatted_input_val in formatted_input_vals:
                try:
                    option = self._map_input_to_option(input_val=formatted_input_val)
                    cnt = 0
                    for o in self.options:
                        if o.selected != -1:
                            cnt += 1
                    option.toggle(max_index=cnt)
                except self.InputInvalidException:
                    invalid_input_vals.append(formatted_input_val)

            for _ in range(len(self.options) + 1):
                Menu.clear_last_line(self._longest_line(prompt_including_answer=_prompt + input_val) + 6)
            if self.numbered:
                selected_plan = 0
                selected_is = 0
                for option in self.options:
                    if option.selected != -1:
                        selected_plan = max(selected_plan, option.selected)
                        selected_is += 1
                offset = selected_plan - selected_is
                for option in self.options:
                    if option.selected > 1 and offset > 0:
                        option.selected -= offset
                self.options = sorted(self.options)
            self._show_options()

            if invalid_input_vals:
                prompt = "Selection (Skipped invalid options: " \
                         f"{str(invalid_input_vals).replace('[', '').replace(']', '')}): "
            else:
                prompt = "Selection: "
            return self.start_selection(_prompt=prompt)

        except RecursionError:
            self.console.print("To many recursions. Aborting process...")
            raise ReferenceError
