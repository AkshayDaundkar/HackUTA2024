from pathlib import Path
import certifi
from pymongo import MongoClient, DESCENDING
from config import DATABASE_INFO, ROOT_PATH

url = f'mongodb+srv://{DATABASE_INFO["db_username"]}:{DATABASE_INFO["db_password"]}@cluster0.v6ud2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

class MongoDBData:
    def __init__(self, db_name, collection_name):
        self.prompt_file = Path(ROOT_PATH, 'config/prompt.xml')
        client = MongoClient(url, tlsCAFile=certifi.where())
        self.collection = self.get_collection(client, db_name, collection_name)

    @staticmethod
    def get_collection(client, db_name, collection_name):
        return client[db_name][collection_name]
    
    def set_prompt_data(self):
        with open(self.prompt_file, 'r') as f:
            post_prompt_data = f.read()
            self.collection.insert_one({
                'prompt': post_prompt_data,
            })

    def get_prompt_data(self, query = {}):
        doc_count = self.collection.count_documents(query)
        assert doc_count > 0, "No prompt data found in the database."
        last_doc = self.collection.find(query).sort([('_id', DESCENDING)]).limit(1)[0]
        assert 'prompt' in last_doc.keys(), "Prompt data not found."
        return last_doc['prompt']

if __name__ == '__main__':
    db = MongoDBData('prompt_db', 'input_prompt')
    # db.set_prompt_data()
    print(db.get_prompt_data())
