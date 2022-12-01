from app.configuration.Database import Database
from app.configuration.DatabaseSessionTransaction import DatabaseSessionTransaction
from app.configuration.dao.dao_command import DaoCommand
from app.configuration.dao.dao_command_collection import DaoCommandCollection
from app.configuration.model.command import Command
from app.configuration.model.command_collection import CommandCollection


class ServiceCommandCollection:
    def __init__(self):
        self.session = Database().session
        self.dbtransaction = DatabaseSessionTransaction(database_session=self.session)

    def get_commands_by_collection_id(self, collection_id: int) -> list[Command]:
        commands = []
        try:
            command_collections = DaoCommandCollection(
                session=self.session
            ).find_by_collection_id(collection_id=collection_id)
        except CommandCollection.NotFoundException:
            raise
        command_collections = sorted(command_collections)
        for command_collection in command_collections:
            try:
                command_collection.index
                commands.append(DaoCommand(session=self.session).find_by_command_id(command_collection.command_id))
            except Command.NotFoundException:
                raise
        return commands
