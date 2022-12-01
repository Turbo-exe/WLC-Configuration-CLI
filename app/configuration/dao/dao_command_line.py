from sqlalchemy import select
from sqlalchemy.orm import Session

from app.configuration.Database import Database
from app.configuration.DatabaseSessionTransaction import DatabaseSessionTransaction
from app.configuration.model.command_line import CommandLine


class DaoCommandLine:
    def __init__(self, session: Session = None):
        self.session = session if session else Database().session
        self.dbtransaction = DatabaseSessionTransaction(database_session=self.session)

    def find_by_command_line_id(self, command_line_id: int) -> CommandLine:
        statement = select(CommandLine).filter_by(id=command_line_id)
        result = self.session.execute(statement=statement).scalars().one_or_none()
        if not result:
            raise CommandLine.NotFoundException
        return result

    def find_by_command_id(self, command_id: int) -> list[CommandLine]:
        statement = select(CommandLine).filter_by(command_id=command_id)
        result = self.session.execute(statement=statement).scalars().all()
        return result

    def add_command_line(self, command_line: CommandLine) -> None:
        with self.dbtransaction.start_transaction() as new_transaction:
            new_transaction.add(command_line)

    def modify_command_line(self, command_line: CommandLine, id_: int, command_id: int, command_line_: str) \
            -> CommandLine:
        with self.dbtransaction.start_transaction() as new_transaction:
            new_transaction.delete(command_line)
            if id_:
                command_line.id = id_
            if command_id:
                command_line.command_id = command_id
            if command_line_:
                command_line.command_line = command_line_
            new_transaction.add(command_line)
        return command_line

    def delete_command_line(self, command_line: CommandLine) -> None:
        with self.dbtransaction.start_transaction() as new_transaction:
            new_transaction.delete(command_line)
