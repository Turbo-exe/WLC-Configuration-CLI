from dataclasses import dataclass
from enum import Enum

from rich.text import Text

from app.cli.cli_components.menu import Menu
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color


@dataclass
class SelectionOption:
    def __init__(self, return_value: any, text_property: str or list, index: int) -> None:
        self.return_value = return_value
        self.text_property = text_property
        self.index = index
        self.text = self._resolve_text_properties(text_property)
        try:
            self.text = getattr(self.return_value, self.text_property)
        except (AttributeError, TypeError):
            self.text = str(text_property)

    text_property: str
    return_value: any
    text: str
    index: int = None

    @staticmethod
    def _resolve_text_property(obj, text_property):
        try:
            if isinstance(text_property, str):
                text = getattr(obj, text_property)
            else:
                text = obj[text_property]
        except (AttributeError, TypeError):
            text = text_property
        return text

    def _resolve_text_properties(self, text_property):
        obj = self.return_value
        if isinstance(text_property, list):
            for prop in text_property:
                obj = self._resolve_text_property(obj=obj, text_property=prop)
        else:
            obj = self._resolve_text_property(obj=obj, text_property=text_property)
        return obj

    def __lt__(self, other):
        return self.index < other.index

    def __eq__(self, other):
        return type(self) == type(other)


class Selection:
    def __init__(self, prompt, console):
        self.console = console
        self.console.print(prompt)
        self.options = []
        self.len_max_index = 0

    def _show_option(self, option: SelectionOption):
        self._update_max_index_length()
        index = self._normalize_index_length(option.index)
        self.console.print(Text.assemble((f"  {index}", str(Color.SELECTION_INDEX.value)),
                                         (f"   {option.text}", "italic" if option.text.find("(") != -1 else "")))

    def _show_options(self):
        self._update_max_index_length()
        for option in self.options:
            self._show_option(option=option)

    def _update_max_index_length(self):
        if self.options:
            self.len_max_index = len(str(max(self.options).index))

    def _register_option(self, option: SelectionOption):
        if not option.index:
            index = 1
            if self.options:
                index = max(self.options) + 1
            option.index = index
        self.options.append(option)
        return option.index

    def register_and_show_options(self, options: dict[int: list[any, any]]) -> None:
        for option_key, option_values in options.items():
            option = SelectionOption(
                index=option_key,
                text_property=option_values[1],
                return_value=option_values[0]
            )
            self._register_option(option=option)
        self._show_options()

    @staticmethod
    def _input_is_index(input_val: int, option: SelectionOption) -> bool:
        try:
            input_val = int(input_val)
            if input_val == option.index:
                return True
            else:
                return False
        except (ValueError, TypeError):
            return False

    @staticmethod
    def _input_is_option_text(input_val: str, option: SelectionOption) -> bool:
        try:
            input_val = str(input_val)
            if input_val.upper() == option.text.upper():
                return True
            else:
                return False
        except (ValueError, TypeError):
            return False

    @staticmethod
    def _option_text_is_enum(option_text: [str, CLIPaths]) -> bool:
        return isinstance(option_text, Enum)

    def _normalize_index_length(self, index: int) -> str:
        spacer_chars = ' ' * (self.len_max_index - len(str(index)))
        return f"{spacer_chars}{index}"

    def _map_input_to_option(self, input_val):
        for option in self.options:
            if self._input_is_index(input_val=input_val, option=option):
                return option
            if self._input_is_option_text(input_val=input_val, option=option):
                return option
        raise self.InputInvalidException

    def start_selection(self, allow_empty_selection=False, _prompt="Selection: "):
        input_val = input(_prompt)
        try:
            option = self._map_input_to_option(input_val=input_val)
            Menu.clear_last_line(len(_prompt) + len(input_val))
            self.console.print(
                Text.assemble(
                    "Selection:",
                    (f"   {option.index}", str(Color.SELECTION_INDEX.value)),
                    (f"   {option.text}", "italic" if option.text.find("(") != -1 else "")
                )
            )
            return option.return_value
        except self.InputInvalidException:
            if allow_empty_selection:
                return
            Menu.clear_last_line(len(_prompt) + len(input_val))
            if _prompt.find("(invalid, try again)") != -1:
                _prompt = "Selection (invalid, try again x2):"
            elif _prompt.find("invalid") != -1:
                _prompt = f"Selection (invalid, try again x{int(_prompt.split('x')[1].split(')')[0]) + 1}):"
            else:
                _prompt = "Selection (invalid, try again): "
            return self.start_selection(allow_empty_selection=allow_empty_selection,
                                        _prompt=_prompt)

    class InputInvalidException(Exception):
        pass
