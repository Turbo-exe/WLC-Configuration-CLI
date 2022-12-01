from sqlalchemy import select
from sqlalchemy.orm import Session

from app.configuration.Database import Database
from app.configuration.DatabaseSessionTransaction import DatabaseSessionTransaction
from app.configuration.model.collection import Collection


class DaoCollection:
    def __init__(self, session: Session = None):
        self.session = session if session else Database().session
        self.dbtransaction = DatabaseSessionTransaction(database_session=self.session)

    def find_by_collection_id(self, collection_id: int) -> Collection:
        statement = select(Collection).filter_by(id=collection_id)
        result = self.session.execute(statement=statement).scalars().one_or_none()
        if not result:
            raise Collection.NotFoundException
        return result

    def find_all_collections(self) -> list[Collection]:
        statement = select(Collection)
        result = self.session.execute(statement=statement).scalars().all()
        return result

    def add_collection(self, collection: Collection) -> None:
        with self.dbtransaction.start_transaction() as new_transaction:
            new_transaction.add(collection)

    def modify_collection(self, collection: Collection, id_: int, name: str, description: str):
        with self.dbtransaction.start_transaction():
            if id_:
                collection.id = id_
            if name:
                collection.name = name
            if description:
                collection.description = description

    def delete_collection(self, collection: Collection) -> None:
        with self.dbtransaction.start_transaction() as new_transaction:
            new_transaction.delete(collection)
