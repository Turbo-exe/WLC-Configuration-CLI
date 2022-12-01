from dataclasses import dataclass
from re import match, compile, error

from sqlalchemy import Column, String, Boolean

from app.configuration.Database import Database


@dataclass
class Variable(Database().base):
    __tablename__ = "variables"
    name = Column(String, primary_key=True, autoincrement=False)
    description = Column(String, autoincrement=False)
    regex_string = Column(String, autoincrement=False)
    is_secret = Column(Boolean, autoincrement=False)
    is_global = Column(Boolean, autoincrement=False)
    ask_for_value_during_execution = Column(Boolean, autoincrement=False)

    def __init__(self, name: str, description: str, regex_string: str,
                 is_secret: bool, is_global: bool, ask_for_value_during_execution: bool):
        self.name = name
        self.description = description
        self.regex_string = regex_string
        self.is_secret = is_secret
        self.is_global = is_global
        self.ask_for_value_during_execution = ask_for_value_during_execution

    @staticmethod
    def validate_name(name: str) -> None:
        try:
            if name:
                int(name)
                raise Variable.InvalidName("Bad name. The name must not be a number!")
        except ValueError:
            pass

    @staticmethod
    def validate_description(description: str) -> None:
        try:
            if description:
                int(description)
                raise Variable.InvalidDescription("Bad description. The description must contain text!")
        except ValueError:
            pass

    @staticmethod
    def validate_regex_string(regex_string: str) -> None:
        try:
            compile(pattern=regex_string)
        except error:
            raise Variable.InvalidRegexString("Bad regex string. The provided pattern is not a valid regex expression!")

    @staticmethod
    def validate_text_with_regex(str_to_validate: str, regex_string: str) -> None:
        if not regex_string:
            return
        if match(regex_string, str_to_validate, flags=0) is None:
            raise Variable.RegexDoesNotMatch("Bad text. The text does not match the regex validation pattern!")

    def __repr__(self):
        return f"<Variable> name={self.name}, " \
               f"description={self.description}, regex_string={self.regex_string}, " \
               f"is_secret={self.is_secret}, is_global={self.is_global}, " \
               f"ask_for_value_during_execution={self.ask_for_value_during_execution}"

    def __eq__(self, other):
        if not isinstance(other, Variable):
            return self.name == other
        return self.name == other.name

    class NotFoundException(Exception):
        pass

    class InvalidName(Exception):
        def __init__(self, message):
            self.message = message

    class InvalidDescription(Exception):
        def __init__(self, message):
            self.message = message

    class InvalidRegexString(Exception):
        def __init__(self, message):
            self.message = message

    class RegexDoesNotMatch(Exception):
        def __init__(self, message):
            self.message = message
