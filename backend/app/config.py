import os
from dotenv import load_dotenv

load_dotenv()

def get_database_url(config_name):

    if config_name == "development":
        database_url = os.getenv("DATABASE_URL")

    elif config_name == "testing":
        database_url = "sqlite:///:memory:"
    
    else:
        raise ValueError("Invalid config_name")

    return database_url

def get_jwt_secret_key():
    return os.getenv("JWT_SECRET_KEY")
