# backend/utils/mongo_client.py
# backend/utils/mongo_client.py
from motor.motor_asyncio import AsyncIOMotorClient
from os import getenv
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = getenv("MONGODB_URI", "mongodb://mongo:27017")

client = AsyncIOMotorClient(MONGODB_URI)
db = client["aidpa_db"]

def get_assistant_collection():
    return db["assistant_collection"]

def get_health_collection():
    return db["health_collection"]


# def insert_health_log(data: dict):
#     return db.health_logs.insert_one(data).inserted_id

# def get_health_logs(limit=7):
#     return list(db.health_logs.find().sort("timestamp", -1).limit(limit))
