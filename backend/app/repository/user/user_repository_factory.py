import os

from app.repository.user.mongo_user_repository import UserRepositoryMongo
from app.repository.user.neo_user_repository import UserRepositoryNeo
from app.repository.user.sql_user_repository import UserRepositorySQL

from app.utility.db_mongo import get_db as get_mongo_db
from app.utility.db_neo import get_neo
from app.utility.db_sql import get_sql_db


def get_user_repository():
    db_mode = os.getenv("DB_MODE", "sql").lower()

    if db_mode == "sql":
        db = next(get_sql_db())
        return UserRepositorySQL(db)
    if db_mode == "mongo":
        db = next(get_mongo_db())
        return UserRepositoryMongo(db)
    if db_mode == "neo":
        driver = get_neo()
        return UserRepositoryNeo(driver)

    raise ValueError(f"Unknown DB_MODE: {db_mode}")
