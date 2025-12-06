from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MongoDBConnector:
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        try:
            connection_string = f"mongodb://{settings.MONGODB_USER}:{
                settings.MONGODB_PASSWORD
            }@{settings.MONGODB_HOST}:{settings.MONGODB_PORT}/"
            self.client = MongoClient(connection_string)
            self.db = self.client[settings.MONGODB_DATABASE]

            self.client.admin.command("ping")
            logger.info("Connected to MongoDB successfully")
        except ConnectionFailure as e:
            logger.error(f"Error connecting to MongoDB: {e}")
            raise

    def insert_documents(self, collection_name, documents):
        try:
            collection = self.db[collection_name]
            if documents:
                result = collection.insert_many(documents, ordered=False)
                logger.info(
                    f"Inserted {len(result.inserted_ids)} documents into {
                        collection_name
                    }"
                )
                return result
            return None
        except PyMongoError as e:
            logger.error(
                f"Error inserting documents into {collection_name}: {e}",
            )
            raise

    def delete_collection(self, collection_name):
        """Delete entire collection"""
        try:
            self.db[collection_name].delete_many({})
            logger.info(f"Cleared collection: {collection_name}")
        except Exception as e:
            logger.error(f"Error clearing collection {collection_name}: {e}")
            raise

    def close(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

