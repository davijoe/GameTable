import os
from contextlib import contextmanager
from pymongo import MongoClient

MONGO_HOST = os.getenv("MONGODB_HOST")
MONGO_PORT = int(os.getenv("MONGODB_PORT"))
MONGO_DB   = os.getenv("MONGO_DATABASE")

_url = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"

client = None

def get_client():
    global client
    if client is None:
        client = MongoClient(_url, serverSelectionTimeoutMS=5000)
    return client

def get_db():
    client = get_client()
    try:
        client.admin.command("ping")
    except Exception:
        raise
    yield client[MONGO_DB]
