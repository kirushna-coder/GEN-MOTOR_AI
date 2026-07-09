from pymongo import MongoClient
from app.config import Config

class Database:
    client = None
    db = None

    @classmethod
    def initialize(cls):
        try:
            cls.client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
            # Verify connection
            cls.client.server_info()
            cls.db = cls.client.get_database()
            print("MongoDB connected successfully")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            cls.db = None

    @classmethod
    def get_db(cls):
        if cls.db is None:
            cls.initialize()
        return cls.db
