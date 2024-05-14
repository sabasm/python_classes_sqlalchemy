import uuid
from datetime import datetime
from collections import namedtuple
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from src.repository_interface import IRepository
from src.sqlalchemy_repository import SQLAlchemyRepository

# Use namedtuple for organizing database table names, making them accessible via attribute-style access
TableNames = namedtuple('TableNames', ['toy', 'owner', 'animal'])
DATABASE_TABLES = TableNames(toy='toys', owner='owners', animal='animals')

# Use namedtuple for organizing foreign key references, improving clarity and maintainability
ForeignKeys = namedtuple('ForeignKeys', ['favorite_toy_id', 'owner_id'])
FOREIGN_KEYS = ForeignKeys(
    favorite_toy_id=f"{DATABASE_TABLES.toy}.id",
    owner_id=f"{DATABASE_TABLES.owner}.id"
)

# Use namedtuple for organizing class names used in relationships, providing clear reference points
ClassNames = namedtuple('ClassNames', ['toy', 'owner', 'animal'])
CLASSES = ClassNames(toy='Toy', owner='Owner', animal='Animal')

# Base class for all SQLAlchemy models
Base = declarative_base()

class BaseEntity:
    """Abstract base class for entities, providing ID and timestamp functionality."""
    def __init__(self, entity_id=None):
        self._id = entity_id if entity_id is not None else str(uuid.uuid4())
        self.timestamps = {
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        raise AttributeError("ID is immutable and cannot be changed.")

    def update_timestamp(self):
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

def main(database_url):
    try:
        db_manager = DatabaseManager(database_url)

        with db_manager.session_scope() as session:
            repository: IRepository = SQLAlchemyRepository(session)

            toy = Toy(id=str(uuid.uuid4()), name="Chew Toy", toy_type="Rubber")
            owner = Owner(id=str(uuid.uuid4()), name="John Doe", contact_info="john@example.com")

            repository.add(toy)
            repository.add(owner)

            baxter = Animal(id=str(uuid.uuid4()), name="Baxter", age=5, favorite_toy_id=toy.id, owner_id=owner.id)

            repository.add(baxter)

            queried_animal = repository.get_by_id(Animal, baxter.id)
            if queried_animal:
                print(f"Animal ID: {queried_animal.id}, Name: {queried_animal.name}, Age: {queried_animal.age}")
            else:
                print("Animal not found.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
