from abc import ABC, abstractmethod

class IRepository(ABC):
    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def get_by_id(self, entity_class, entity_id):
        pass

    @abstractmethod
    def update(self, entity_class, entity_id, **kwargs):
        pass

    @abstractmethod
    def delete(self, entity_class, entity_id):
        pass
