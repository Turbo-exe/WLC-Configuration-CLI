from rich.console import Console

from app.cli.enum.color import Color


def wait_for_user_to_continue(console: Console, prompt="Press Enter to continue..."):
    console.print(prompt, end="", style=str(Color.PROCEED.value))
    input()
