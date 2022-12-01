from app.configuration.model.command import Command
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.configuration.Database import Database
from app.configuration.DatabaseSessionTransaction import DatabaseSessionTransaction


class DaoCommand:
    def __init__(self, session: Session = None):
        self.session = session if session else Database().session
        self.dbtransaction = DatabaseSessionTransaction(database_session=self.session)

    def find_by_command_id(self, command_id: int) -> Command:
        statement = select(Command).filter_by(id=command_id)
        result = self.session.execute(statement=statement).scalars().one_or_none()
        if not result:
            raise Command.NotFoundException
        return result

    def find_all_commands(self) -> list[Command]:
        statement = select(Command)
        result = self.session.execute(statement=statement).scalars().all()
        return result

    def add_command(self, command: Command) -> None:
        with self.dbtransaction.start_transaction() as new_transaction:
            new_transaction.add(command)

    def modify_command(self, command: Command, id_: int, name: str, description: str) -> Command:
        with self.dbtransaction.start_transaction() as new_transaction:
            new_transaction.delete(command)
            if id_:
                command.id = id_
            if name:
                command.name = name
            if description:
                command.description = description
            new_transaction.add(command)
            return command

    def delete_command(self, command: Command) -> None:
        with self.dbtransaction.start_transaction() as new_transaction:
            new_transaction.delete(command)
