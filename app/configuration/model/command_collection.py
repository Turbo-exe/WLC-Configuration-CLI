from dataclasses import dataclass

from sqlalchemy import Column, Integer, ForeignKey

from app.configuration.Database import Database


@dataclass
class CommandCollection(Database().base):
    __tablename__ = "command_collection"
    collection_id = Column(Integer, ForeignKey("collections.id"), primary_key=True, autoincrement=False)
    command_id = Column(Integer, ForeignKey("commands.id"), primary_key=True, autoincrement=False)
    index = Column(Integer, autoincrement=False)

    def __init__(self, collection_id: int, command_id: int, index: int):
        self.collection_id = collection_id
        self.command_id = command_id
        self.index = index

    def __repr__(self):
        return f"<CommandCollection> collection_id={self.collection_id}, " \
               f"command_id={self.command_id}, index={self.index}"

    def __lt__(self, other):
        if not isinstance(other, CommandCollection):
            raise TypeError
        return self.index < other.index

    class NotFoundException(Exception):
        pass
