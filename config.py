import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    EXCHANGE_RATE_API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')