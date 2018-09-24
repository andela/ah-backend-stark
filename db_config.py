import os
from dotenv import load_dotenv

def get_database_url():
    """ 
    gets the environment variable for the database url if it exists or sets it
    by reading the .env file configuration and then returns it

    """
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        current_dir = os.getcwd()
        load_dotenv(os.path.join(current_dir,'.env'))
        database_url = os.getenv('DATABASE_URL')

    return database_url