from sqlalchemy.orm import Session
from .repository_interface import IRepository

class SQLAlchemyRepository(IRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()

    def get_by_id(self, entity_class, entity_id):
        return self.session.query(entity_class).filter_by(id=entity_id).first()

    def update(self, entity_class, entity_id, **kwargs):
        entity = self.get_by_id(entity_class, entity_id)
        if entity:
            for key, value in kwargs.items():
                setattr(entity, key, value)
            self.session.commit()

    def delete(self, entity_class, entity_id):
        entity = self.get_by_id(entity_class, entity_id)
        if entity:
            self.session.delete(entity)
            self.session.commit()
