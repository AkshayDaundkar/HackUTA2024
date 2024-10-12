# config.py
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access API keys and DB connection
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
