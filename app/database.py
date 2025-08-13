import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "chatdb")

client = AsyncIOMotorClient(DATABASE_URL)
db = client[DB_NAME]
