import uuid
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from src.repository_interface import IRepository
from src.sqlalchemy_repository import SQLAlchemyRepository
from src.constants.database_constants import DATABASE_TABLES, FOREIGN_KEYS, CLASSES

# Base class for all SQLAlchemy models
Base = declarative_base()

class BaseEntity:
    """Abstract base class for entities, providing ID and timestamp functionality."""

    def __init__(self, entity_id=None):
        """
        Initialize the BaseEntity.

        Args:
            entity_id (str): The unique identifier for the entity. If None, a new UUID is generated.
        """
        self._id = entity_id if entity_id is not None else str(uuid.uuid4())
        self.timestamps = {
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }

    @property
    def id(self):
        """ID property that is immutable once set."""
        return self._id

    @id.setter
    def id(self, value):
        """Prevent changes to ID after it's set initially."""
        raise AttributeError("ID is immutable and cannot be changed.")

    def update_timestamp(self):
        """Update the timestamp to the current time when called."""
        self.timestamps['updated_at'] = datetime.now()

class Toy(Base):
    """Model for Toy, representing toy data."""
    __tablename__ = DATABASE_TABLES.toy
    id = Column(String, primary_key=True)
    name = Column(String)
    toy_type = Column(String)

class Owner(Base):
    """Model for Owner, representing owner data."""
    __tablename__ = DATABASE_TABLES.owner
    id = Column(String, primary_key=True)
    name = Column(String)
    contact_info = Column(String)

class Animal(Base):
    """Model for Animal, representing animal data with relationships to Toy and Owner."""
    __tablename__ = DATABASE_TABLES.animal
    id = Column(String, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    favorite_toy_id = Column(String, ForeignKey(FOREIGN_KEYS.favorite_toy_id))
    owner_id = Column(String, ForeignKey(FOREIGN_KEYS.owner_id))
    favorite_toy = relationship(CLASSES.toy)
    owner = relationship(CLASSES.owner)

class DatabaseManager:
    """Database manager class for handling database operations."""

    def __init__(self, database_url):
        """
        Initialize the DatabaseManager.

        Args:
            database_url (str): The database URL to connect to.
        """
        self.engine = create_engine(database_url, pool_pre_ping=True, pool_recycle=3600)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session_scope(self):
        """
        Provide a transactional scope around a series of operations.

        Yields:
            sqlalchemy.orm.Session: A SQLAlchemy session.
        """
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

def main(database_url):
    """
    Main function to perform database operations.

    Args:
        database_url (str): The database URL to connect to.
    """
    try:
        db_manager = DatabaseManager(database_url)

        with db_manager.session_scope() as session:
            repository: IRepository = SQLAlchemyRepository(session)

            # Create instances of Toy and Owner
            toy = Toy(id=str(uuid.uuid4()), name="Chew Toy", toy_type="Rubber")
            owner = Owner(id=str(uuid.uuid4()), name="John Doe", contact_info="john@example.com")

            # Add Toy and Owner to the database
            repository.add(toy)
            repository.add(owner)

            # Create Animal instance after Toy and Owner are added to the database
            baxter = Animal(id=str(uuid.uuid4()), name="Baxter", age=5, favorite_toy_id=toy.id, owner_id=owner.id)

            # Add Animal to the database
            repository.add(baxter)

            # Query the database for an Animal with a specific ID and display its information
            queried_animal = repository.get_by_id(Animal, baxter.id)
            if queried_animal:
                print(f"Animal ID: {queried_animal.id}, Name: {queried_animal.name}, Age: {queried_animal.age}")
            else:
                print("Animal not found.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
