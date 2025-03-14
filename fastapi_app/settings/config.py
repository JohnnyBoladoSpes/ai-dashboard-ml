import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/ai_data")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
