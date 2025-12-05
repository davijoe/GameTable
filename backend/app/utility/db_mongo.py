import os
from contextlib import contextmanager
from pymongo import MongoClient

MONGO_HOST = os.getenv("MONGODB_HOST")
MONGO_PORT = os.getenv("MONGODB_PORT")
MONGO_DB   = os.getenv("MONGODB_DATABASE")
MONGO_USER = os.getenv("MONGODB_USER")
MONGO_PASS = os.getenv("MONGODB_PASSWORD")

_url = (
    f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"
    f"{MONGO_DB}?authSource=admin"
)

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
        yield client[MONGO_DB]
    finally:
        pass
