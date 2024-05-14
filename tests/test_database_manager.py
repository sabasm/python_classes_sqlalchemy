import unittest
from unittest.mock import patch
from src.services.database_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):

    @patch('src.services.database_manager.create_engine')
    @patch('src.services.database_manager.sessionmaker')
    def test_database_initialization(self, mock_sessionmaker, mock_create_engine):
        database_url = 'sqlite:///test.db'
        db_manager = DatabaseManager(database_url)
        mock_create_engine.assert_called_with(database_url, pool_pre_ping=True, pool_recycle=3600)
        self.assertTrue(mock_sessionmaker.called)
        self.assertTrue(db_manager)

if __name__ == '__main__':
    unittest.main()
