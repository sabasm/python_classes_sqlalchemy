import os
import uuid
from datetime import datetime
from abc import ABC, abstractmethod
from collections import namedtuple
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configure the database URL from environment variables or use a default if not specified
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///mydatabase.db')

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

class BaseEntity(ABC):
    """Abstract base class for entities, providing ID and timestamp functionality."""
    def __init__(self, entity_id=None):
        # Assign a unique ID upon creation, or use a given ID (for existing entities)
        self._id = entity_id if entity_id is not None else str(uuid.uuid4())
        # Initialize creation and update timestamps
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

    @abstractmethod
    def display_entity_info(self):
        """Abstract method to display information about the entity. Must be implemented by subclasses."""
        pass

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

    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
        # Create all tables
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
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

class Repository:
    """Repository class for abstracting database operations."""

    def __init__(self, session):
        self.session = session

    def add_entity(self, entity):
        """Add an entity to the database."""
        self.session.add(entity)
        self.session.commit()

    def query_entity_by_id(self, entity_class, entity_id):
        """Query an entity by its ID."""
        return self.session.query(entity_class).filter_by(id=entity_id).first()

    def update_entity(self, entity_class, entity_id, **kwargs):
        """Update an entity in the database."""
        entity = self.session.query(entity_class).filter_by(id=entity_id).first()
        if entity:
            for key, value in kwargs.items():
                setattr(entity, key, value)
            entity.update_timestamp()
            self.session.commit()
        else:
            print(f"Entity with id {entity_id} not found.")

    def delete_entity(self, entity_class, entity_id):
        """Delete an entity from the database."""
        entity = self.session.query(entity_class).filter_by(id=entity_id).first()
        if entity:
            self.session.delete(entity)
            self.session.commit()
        else:
            print(f"Entity with id {entity_id} not found.")

if __name__ == '__main__':
    try:
        db_manager = DatabaseManager()

        with db_manager.session_scope() as session:
            repository = Repository(session)

            # Create instances of Toy and Owner
            toy = Toy(id=str(uuid.uuid4()), name="Chew Toy", toy_type="Rubber")
            owner = Owner(id=str(uuid.uuid4()), name="John Doe", contact_info="john@example.com")

            # Add Toy and Owner to the database
            repository.add_entity(toy)
            repository.add_entity(owner)

            # Create Animal instance after Toy and Owner are added to the database
            baxter = Animal(id=str(uuid.uuid4()), name="Baxter", age=5, favorite_toy_id=toy.id, owner_id=owner.id)

            # Add Animal to the database
            repository.add_entity(baxter)

            # Query the database for an Animal with a specific ID and display its information
            queried_animal = repository.query_entity_by_id(Animal, baxter.id)
            if queried_animal:
                print(f"Animal ID: {queried_animal.id}, Name: {queried_animal.name}, Age: {queried_animal.age}")
            else:
                print("Animal not found.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
