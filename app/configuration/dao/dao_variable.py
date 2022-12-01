from sqlalchemy import select
from sqlalchemy.orm import Session

from app.configuration.Database import Database
from app.configuration.DatabaseSessionTransaction import DatabaseSessionTransaction
from app.configuration.model.variable import Variable


class DaoVariable:
    def __init__(self, session: Session = None):
        self.session = session if session else Database().session
        self.dbtransaction = DatabaseSessionTransaction(database_session=self.session)

    def find_by_variable_name(self, variable_name: str) -> Variable:
        statement = select(Variable).filter_by(name=variable_name)
        result = self.session.execute(statement=statement).scalars().one_or_none()
        if not result:
            raise Variable.NotFoundException
        return result

    def find_all_variables(self) -> list[Variable]:
        statement = select(Variable)
        result = self.session.execute(statement=statement).scalars().all()
        return result

    def add_variable(self, variable: Variable) -> None:
        with self.dbtransaction.start_transaction() as new_transaction:
            new_transaction.add(variable)

    @staticmethod
    def modify_variable(variable: Variable, name: str, description: str, regex_string: str, is_secret: bool,
                        is_global: bool, ask_for_value_during_execution: bool):
        if name:
            variable.name = name
        if description:
            variable.description = description
        if regex_string:
            variable.regex_string = regex_string
        if is_secret is not None:
            variable.is_secret = is_secret
        if is_global is not None:
            variable.is_global = is_global
        if ask_for_value_during_execution is not None:
            variable.ask_for_value_during_execution = ask_for_value_during_execution

    def delete_variable(self, variable: Variable) -> None:
        with self.dbtransaction.start_transaction() as new_transaction:
            new_transaction.delete(variable)

    @staticmethod
    def string_contains_variable(text: str):
        return text.find("{{") != -1 and text.find("}}") != -1

    @staticmethod
    def reformat_variables_in_string(text: str):
        if not DaoVariable.string_contains_variable(text=text):
            return
        for _ in range(text.count("{{")):
            for i, char in enumerate(text):
                if char == "{" and text[i+1] == "{":
                    text = text[0:i] + text[i:text.find("}}", i)].lower() + text[text.find("}}", i):len(text)]
        return text

    def get_variables_from_string(self, text: str) -> list[Variable]:
        if not DaoVariable.string_contains_variable(text=text):
            return []
        variables = []
        for _ in range(text.count("{{")):
            for i, char in enumerate(text):
                if char == "{" and text[i+1] == "{":
                    variable_name = text[i+2:text.find("}}", i)].lower()
                    if isinstance((variable := self.find_by_variable_name(variable_name=variable_name)), Variable):
                        if variable not in variables:
                            variables.append(variable)
        return variables
