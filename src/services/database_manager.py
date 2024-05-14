from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from src.models.models import Base

class DatabaseManager:
    """Database manager class for handling database operations."""

    def __init__(self, database_url):
        self.engine = create_engine(database_url, pool_pre_ping=True, pool_recycle=3600)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Session rollback because of error: {e}")
            raise
        finally:
            session.close()
