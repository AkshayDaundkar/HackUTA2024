# database.py
from pymongo import MongoClient
from config import MONGO_URI

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client['market_strategy_db']
prompts_collection = db['prompts']

def save_prompt(prompt_data):
    # Save prompt data to MongoDB
    prompts_collection.insert_one(prompt_data)

def get_all_prompts():
    # Retrieve all prompts from MongoDB
    return list(prompts_collection.find())
