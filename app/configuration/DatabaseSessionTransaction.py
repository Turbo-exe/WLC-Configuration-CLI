from contextlib import contextmanager
from sqlalchemy.orm import Session


class DatabaseSessionTransaction:
    def __init__(self, database_session: Session):
        self.database_session = database_session

    @contextmanager
    def start_transaction(self):
        try:
            yield self.database_session
        except (Exception, SystemExit):
            self.database_session.rollback()
        else:
            try:
                self.database_session.commit()
            except (Exception, SystemExit):
                self.database_session.rollback()
                raise
