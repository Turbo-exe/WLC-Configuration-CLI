from dataclasses import dataclass

from sqlalchemy import Column, Integer, String

from app.configuration.Database import Database


@dataclass
class Collection(Database().base):
    __tablename__ = "collections"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, autoincrement=False)
    description = Column(String, autoincrement=False)

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @staticmethod
    def validate_name(name: str) -> None:
        try:
            if name:
                int(name)
                raise Collection.InvalidName("Bad name. The name must not be a number!")
        except ValueError:
            pass

    @staticmethod
    def validate_description(description: str) -> None:
        try:
            if description:
                int(description)
                raise Collection.InvalidDescription("Bad description. The description must contain text!")
        except ValueError:
            pass

    def __repr__(self):
        return f"<Collection> id={self.id}, name={self.name}, description={self.description}"

    class NotFoundException(Exception):
        pass

    class InvalidName(Exception):
        def __init__(self, message):
            self.message = message

    class InvalidDescription(Exception):
        def __init__(self, message):
            self.message = message
