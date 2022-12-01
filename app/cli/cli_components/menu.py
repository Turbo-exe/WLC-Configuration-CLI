from os import system
from platform import platform

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from app.cli.enum.cli_options import CLIPaths


class Menu:
    menus = []
    name = None

    def __init__(self, path, console: Console):
        Menu.menus.append(path)
        self.console = console
        self.path = path
        self.name = path[-1]

    def _show_header(self) -> None:
        self.console.print(Panel(Text("\nWLC Configuration CLI.\n", justify="center")))
        text = ""
        for mode in tuple(self.path):
            text = f"{text} -> {mode}"
        self.console.print(Panel(Text(text, justify="left")))

    def start(self):
        pass

    @staticmethod
    def _selection_option_is_show_able(option):
        try:
            _ = option.start
            return True
        except AttributeError:
            return False

    def reset_screen(self) -> None:
        self.clear_screen()
        self._show_header()

    def horizontal_spacer(self) -> None:
        self.console.print(Panel(""))

    @staticmethod
    def clear_screen():
        if platform == "linux":
            system("clear")
        else:
            system("cls")

    @staticmethod
    def clear_last_line(len_last_line: int = 30):
        print("\033[A" + (" " * len_last_line) + "\033[A")

    def _decide_upon_selection(self, selected_option):
        if self._selection_option_is_show_able(option=selected_option):
            selected_option.start()
            self.start()
        elif selected_option == CLIPaths.BACK:
            return
