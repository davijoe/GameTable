import os

from app.repository.review.mongo_review_repository import ReviewRepositoryMongo
from app.repository.review.neo_review_repository import ReviewRepositoryNeo
from app.repository.review.sql_review_repository import ReviewRepositorySQL

from app.utility.db_mongo import get_db as get_mongo_db
from app.utility.db_neo import get_neo
from app.utility.db_sql import get_sql_db


def get_review_repository():
    db_mode = os.getenv("DB_MODE", "sql").lower()

    if db_mode == "sql":
        db = next(get_sql_db())
        return ReviewRepositorySQL(db)
    if db_mode == "mongo":
        db = next(get_mongo_db())
        return ReviewRepositoryMongo(db)
    if db_mode == "neo":
        driver = get_neo()
        return ReviewRepositoryNeo(driver)

    raise ValueError(f"Unknown DB_MODE: {db_mode}")
