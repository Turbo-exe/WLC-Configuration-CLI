class YesNo:
    decision: bool

    def __init__(self, console, prompt="Are you sure? [y/n]: "):
        prompt = self._normalize_prompt(prompt=prompt)
        self.console = console
        self.console.print(prompt, end="")
        self.decision = self._process_answer(input())

    @staticmethod
    def _normalize_prompt(prompt):
        prompt = prompt.rstrip()
        if prompt.find("(y/n)") == -1:
            prompt += " (y/n): "
        return prompt

    @staticmethod
    def _process_answer(answer):
        if answer == "y":
            return True
        else:
            return False
