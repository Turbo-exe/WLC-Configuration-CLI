from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from app.configuration.Database import Database


@dataclass
class CommandLine(Database().base):
    __tablename__ = "command_lines"
    id = Column(Integer, primary_key=True)
    command_id = Column(Integer, ForeignKey("commands.id"), primary_key=True, autoincrement=False)
    command_line = Column(String, autoincrement=False)

    def __init__(self, id_: int, command_id: int, command_line: str):
        self.id = id_
        self.command_id = command_id
        self.command_line = command_line

    def __repr__(self):
        return f"<CommandLine> id={self.id}, command_id={self.command_id}, command_line={self.command_line}"

    class NotFoundException(Exception):
        pass
