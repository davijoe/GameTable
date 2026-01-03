import os

from app.repository.publisher.mongo_publisher_repository import PublisherRepositoryMongo
from app.repository.publisher.neo_publisher_repository import PublisherRepositoryNeo
from app.repository.publisher.sql_publisher_repository import PublisherRepositorySQL
from app.utility.db_mongo import get_db as get_mongo_db
from app.utility.db_neo import get_neo
from app.utility.db_sql import get_sql_db


def get_publisher_repository():
    db_mode = os.getenv("DB_MODE", "sql").lower()

    if db_mode == "sql":
        db = next(get_sql_db())
        return PublisherRepositorySQL(db)
    if db_mode == "mongo":
        db = next(get_mongo_db())
        return PublisherRepositoryMongo(db)
    if db_mode == "neo":
        driver = get_neo()
        return PublisherRepositoryNeo(driver)

    raise ValueError(f"Unknown DB_MODE: {db_mode}")
