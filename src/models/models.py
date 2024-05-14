import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from src.constants.database_constants import DATABASE_TABLES, FOREIGN_KEYS, CLASSES

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
