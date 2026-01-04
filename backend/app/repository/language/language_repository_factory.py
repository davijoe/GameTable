import os

from app.repository.language.mongo_language_repository import LanguageRepositoryMongo
from app.repository.language.neo_language_repository import LanguageRepositoryNeo
from app.repository.language.sql_language_repository import LanguageRepositorySQL
from app.utility.db_mongo import get_db as get_mongo_db
from app.utility.db_neo import get_neo
from app.utility.db_sql import get_sql_db


def get_language_repository():
    db_mode = os.getenv("DB_MODE", "sql").lower()
    print("------------------------------------")
    print("DB_MODE seen by backend:", db_mode)
    print("------------------------------------")

    if db_mode == "sql":
        db = next(get_sql_db())
        return LanguageRepositorySQL(db)

    if db_mode == "mongo":
        db = next(get_mongo_db())
        return LanguageRepositoryMongo(db)

    if db_mode == "neo":
        driver = get_neo()
        return LanguageRepositoryNeo(driver)

    raise ValueError(f"Unknown DB_MODE: {db_mode}")
