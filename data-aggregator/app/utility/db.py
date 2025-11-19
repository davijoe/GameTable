from pymongo import MongoClient

from app.settings import settings


MONGO_USER = settings.mongo_root_username
MONGO_PASS = settings.mongo_root_password


def get_mongo_collection():
    uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@localhost:27017/gametable?authSource=admin"
    client = MongoClient(uri)
    db = client["gametable"]
    return db["bgg_games"]
