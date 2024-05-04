# Python SQLAlchemy Application 💡

This application demonstrates a basic ORM setup using SQLAlchemy in Python. It manages data related to toys, owners, and animals, showcasing relationships and basic CRUD operations.

## Setup 📁
### Prerequisites
- Python 3.8 or higher
- pip and virtual environment (venv)

### Installation 🚀
1. **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

Create a virtual environment:
```bash
# For Unix/macOS
python3 -m venv venv
```
For Windows:
```
python -m venv venv
```
Activate the virtual environment:
```bash
# For Unix/macOS
source venv/bin/activate
```
For Windows:
```
venv\Scripts\activate
```
Install the required packages:
```bash
pip install -r requirements.txt
```
Set up the environment variables:
Create a `.env` file in the root directory.
Add the following line to specify your database URL (adjust the value as necessary):
```
DATABASE_URL=sqlite:///mydatabase.db
```
Running the Application 💻
To run the application, execute the following command:
```bash
python main.py
```
This will initiate the script, create required database tables if they do not exist, and perform predefined tasks such as adding and querying entries.

## Features 🎯
- Utilizes SQLAlchemy for ORM.
- Demonstrates relationships between tables.
- Shows how to perform basic CRUD operations in SQLAlchemy.

## License 📜
This project is open-sourced under the MIT license.