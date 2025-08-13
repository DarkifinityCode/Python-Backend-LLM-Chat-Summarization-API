import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

# Accept both SRV and standard URLs; default to local Mongo.
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017/chatdb")

_client = AsyncIOMotorClient(DATABASE_URL)

# Choose DB name:
# - If SRV string without explicit DB, default to "chatdb"
# - If standard URL includes /dbname, Mongo selects it automatically
def _get_db_name():
    if "/" in DATABASE_URL.rsplit("@", 1)[-1]:
        # ...mongodb.net/<maybe-db>?...
        tail = DATABASE_URL.rsplit("/", 1)[-1]
        name = tail.split("?")[0]
        return name or "chatdb"
    # simple/local style (mongodb://host:port/chatdb)
    tail = DATABASE_URL.rsplit("/", 1)[-1]
    return tail or "chatdb"

_db_name = _get_db_name()
db = _client[_db_name]
