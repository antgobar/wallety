from pymongo import MongoClient

from .config import Config


class MongoDb:
    _instance = None

    def __new__(cls, uri):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        cls._instance = MongoClient(uri)
        return cls._instance


def _transactions_collection():
    client = MongoDb(Config.MONGO_URI)
    database = client["wallety"]
    return database["transactions"]


class Transactions:
    def __init__(self):
        self.collection = _transactions_collection()
        
    def refresh_transactions(self, new_transactions: list[dict]) -> dict:
        deletion = self.collection.delete_many({})
        
        
        inserted = self.collection.insert_many(new_transactions)
        
        return {
            "deleted": deletion.deleted_count,
            "added": len(inserted.inserted_ids)
        }
    
    def get_transactions(self):
        return self.collection.find_many({})