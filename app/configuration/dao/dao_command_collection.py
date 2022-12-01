from sqlalchemy import select
from sqlalchemy.orm import Session

from app.configuration.Database import Database
from app.configuration.DatabaseSessionTransaction import DatabaseSessionTransaction
from app.configuration.model.command_collection import CommandCollection


class DaoCommandCollection:
    def __init__(self, session: Session = None):
        self.session = session if session else Database().session
        self.dbtransaction = DatabaseSessionTransaction(database_session=self.session)

    def find_by_command_id_and_collection_id(self, command_id: int, collection_id: int) -> CommandCollection:
        statement = select(CommandCollection).filter_by(
            collection_id=collection_id,
            command_id=command_id
        )
        result = self.session.execute(statement=statement).scalars().one_or_none()
        if not result:
            raise CommandCollection.NotFoundException
        return result

    def find_by_collection_id(self, collection_id: int) -> list[CommandCollection]:
        statement = select(CommandCollection).filter_by(
            collection_id=collection_id
        )
        result = self.session.execute(statement=statement).scalars().all()
        if not result:
            raise CommandCollection.NotFoundException
        return result

    def find_by_command_id(self, command_id: int) -> list[CommandCollection]:
        statement = select(CommandCollection).filter_by(
            command_id=command_id
        )
        result = self.session.execute(statement=statement).scalars().all()
        if not result:
            raise CommandCollection.NotFoundException
        return result

    def find_all_command_collections(self) -> list[CommandCollection]:
        statement = select(CommandCollection)
        result = self.session.execute(statement=statement).scalars().all()
        return result

    def add_command_collection(self, command_collection: CommandCollection) -> None:
        with self.dbtransaction.start_transaction() as new_transaction:
            new_transaction.add(command_collection)

    def delete_command_collection(self, command_collection: CommandCollection) -> None:
        with self.dbtransaction.start_transaction() as new_transaction:
            new_transaction.delete(command_collection)
