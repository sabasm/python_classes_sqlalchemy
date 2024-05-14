import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configure the database URL from environment variables or use a default if not specified
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///mydatabase.db')

if __name__ == '__main__':
    from src.main import main
    main(DATABASE_URL)
