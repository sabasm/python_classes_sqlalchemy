import uuid
from src.models.models import Toy, Owner, Animal
from src.services.database_manager import DatabaseManager
from src.repository_interface import IRepository
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository

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

if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv()
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///mydatabase.db')
    main(DATABASE_URL)
