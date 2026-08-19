import os
from dotenv import load_dotenv

load_dotenv()

def get_database_url(config_name):

    if config_name == "development":
        database_url = os.getenv("DATABASE_URL")
    
    else:
        raise ValueError("Invalid config_name")

    return database_url
    