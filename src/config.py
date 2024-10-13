# configjj.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access API keys and DB connection
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
ROOT_PATH = Path(__file__).parent.parent
DATABASE_INFO = {
  'db_username': 'hackuta',
  'db_password': 'hello12345'
}

