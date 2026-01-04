import os

from app.utility.db_mongo import get_db as get_mongo_db
from app.utility.db_neo import get_neo
from app.utility.db_sql import get_sql_db

DB_MODE = os.getenv("DB_MODE", "sql").lower()


def get_designer_repository():
    if DB_MODE == "sql":
        db = next(get_sql_db())
        return (db)
    elif DB_MODE == "mongo":
        db = next(get_mongo_db())
        return (db)
    elif DB_MODE == "neo":
        db = get_neo()
        return (db)

    raise ValueError(f"Unknown DB_MODE: {DB_MODE}")
