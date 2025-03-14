from pymongo import MongoClient

from fastapi_app.settings.config import MONGO_URI


class DatabaseConnection:
    """Handles MongoDB connection as a Singleton class."""

    _instance = None

    def __new__(cls, *args, **kwargs) -> "DatabaseConnection":
        if not cls._instance:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._init_db(*args, **kwargs)
        return cls._instance

    def _init_db(self, uri: str = MONGO_URI, db_name: str = "ai_data") -> None:
        """Initialize the MongoDB connection."""
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str) -> MongoClient:
        """Retrieve a collection from the database."""
        return self.db[collection_name]


# Create a singleton instance
mongo_connection = DatabaseConnection()

if __name__ == "__main__":
    print("MongoDB connection successful:", mongo_connection.db.list_collection_names())
