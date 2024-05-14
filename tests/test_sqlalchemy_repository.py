import unittest
from unittest.mock import MagicMock
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository
from src.models.models import Toy, Owner, Animal

class TestSQLAlchemyRepository(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock()
        self.repository = SQLAlchemyRepository(self.session)

    def test_add_entity(self):
        toy = Toy(id='1', name='Toy', toy_type='Type')
        self.repository.add(toy)
        self.session.add.assert_called_with(toy)
        self.session.commit.assert_called_once()

    def test_get_by_id(self):
        self.repository.get_by_id(Toy, '1')
        self.session.query(Toy).filter_by(id='1').first.assert_called_once()

    def test_update_entity(self):
        toy = Toy(id='1', name='Toy', toy_type='Type')
        self.session.query(Toy).filter_by(id='1').first.return_value = toy
        self.repository.update(Toy, '1', name='Updated Toy', toy_type='Updated Type')
        self.assertEqual(toy.name, 'Updated Toy')
        self.assertEqual(toy.toy_type, 'Updated Type')
        self.session.commit.assert_called_once()

    def test_delete_entity(self):
        toy = Toy(id='1', name='Toy', toy_type='Type')
        self.session.query(Toy).filter_by(id='1').first.return_value = toy
        self.repository.delete(Toy, '1')
        self.session.delete.assert_called_with(toy)
        self.session.commit.assert_called_once()

    def test_add_owner(self):
        owner = Owner(id='1', name='John Doe', contact_info='john@example.com')
        self.repository.add(owner)
        self.session.add.assert_called_with(owner)
        self.session.commit.assert_called_once()

    def test_add_animal(self):
        toy = Toy(id='1', name='Chew Toy', toy_type='Rubber')
        owner = Owner(id='2', name='John Doe', contact_info='john@example.com')
        animal = Animal(id='3', name='Baxter', age=5, favorite_toy_id=toy.id, owner_id=owner.id)
        self.repository.add(animal)
        self.session.add.assert_called_with(animal)
        self.session.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
