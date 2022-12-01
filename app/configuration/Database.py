from dataclasses import dataclass
from os import getcwd
from os.path import exists, join

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base


class Singleton(object):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instances[cls]


@dataclass
class Database(Singleton):
    PATH = "app/configuration/configurations.db"

    def __init__(self):
        if not hasattr(self, "base"):
            self.base = declarative_base()
        if not hasattr(self, "engine"):
            self.engine = create_engine("sqlite+pysqlite:///app/configuration/configurations.db")
        if not hasattr(self, "session"):
            self.session = Session(bind=self.engine, autoflush=True, autocommit=False)


def _check_if_db_exists(path: str) -> bool:
    return exists(path=join(getcwd(), path))


# noinspection PyUnresolvedReferences
def _create_database():
    # KEEP UNUSED IMPORTS (NEEDED FOR DATABASE CREATION)
    try:
        from app.configuration.model.command import Command
    except ImportError:
        pass
    try:
        from app.configuration.model.command_collection import CommandCollection
    except ImportError:
        pass
    try:
        from app.configuration.model.collection import Collection
    except ImportError:
        pass
    try:
        from app.configuration.model.command_line import CommandLine
    except ImportError:
        pass
    try:
        from app.configuration.model.variable import Variable
    except ImportError:
        pass
    db = Database()
    db.base.metadata.create_all(db.engine)
