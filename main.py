import os
import uuid
from datetime import datetime
from abc import ABC, abstractmethod
from collections import namedtuple
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
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

# Set up the database engine and create all tables
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    # Create instances of Toy, Owner, and Animal
    toy = Toy(id=str(uuid.uuid4()), name="Chew Toy", toy_type="Rubber")
    owner = Owner(id=str(uuid.uuid4()), name="John Doe", contact_info="john@example.com")
    baxter = Animal(id=str(uuid.uuid4()), name="Baxter", age=5, favorite_toy=toy, owner=owner)

    # Add instances to the session and commit them to the database
    session.add_all([toy, owner, baxter])
    session.commit()

    # Query the database for an Animal named 'Baxter' and display its information
    queried_animal = session.query(Animal).filter_by(name="Baxter").first()
    print(f"Animal ID: {queried_animal.id}, Name: {queried_animal.name}, Age: {queried_animal.age}")

    session.close()  # Close the session
