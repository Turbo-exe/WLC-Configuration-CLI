from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from app.cli.cli_tree.cli_main_menu.cli_main_menu import MenuMainMenu
from app.cli.enum.cli_options import CLIPaths
from app.cli.enum.color import Color


class CLI:
    def __init__(self):
        rprint(Panel(Text("\nWLC Configuration CLI.\n", justify="center")))
        self.prev_mode = CLIPaths.MAIN_MENU
        self.mode = CLIPaths.MAIN_MENU
        self.console = Console()
        self.data = None
        self.start()

    def start(self):
        while True:
            try:
                main_menu = MenuMainMenu(console=self.console)
                main_menu.start()
            except KeyboardInterrupt:
                try:
                    self.console.print("\n")
                    self.console.print(Panel("Press Ctrl+C again to quit    OR    Press enter to get to the main menu",
                                             style=str(Color.FAIL.value) + " bold blink"),
                                       justify="center")
                    self.console.input()
                except KeyboardInterrupt:
                    exit()


if __name__ == '__main__':
    CLI()
