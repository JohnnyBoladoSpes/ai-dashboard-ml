from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from fastapi_app.settings.config import MONGO_URI


class DatabaseConnection:
    """Handles MongoDB connection as a Singleton class with authentication."""

    _instance = None

    def __new__(cls, *args, **kwargs) -> "DatabaseConnection":
        if not cls._instance:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._init_db(*args, **kwargs)
        return cls._instance

    def _init_db(self, uri: str = MONGO_URI, db_name: str = "ai_data") -> None:
        """Initialize the MongoDB connection with authentication."""
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.db = self.client[db_name]
            # Test connection
            self.client.server_info()
            print("MongoDB connection successful")
        except ServerSelectionTimeoutError as error:
            print(f"Error: Unable to connect to MongoDB. {error}")

    def get_collection(self, collection_name: str):
        """Retrieve a collection from the database."""
        return self.db[collection_name]


# Create a singleton instance
mongo_connection = DatabaseConnection()

if __name__ == "__main__":
    print("Available collections:", mongo_connection.db.list_collection_names())
