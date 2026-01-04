import os

from app.repository.mechanic.mongo_mechanic_repository import MechanicRepositoryMongo
from app.repository.mechanic.neo_mechanic_repository import MechanicRepositoryNeo
from app.repository.mechanic.sql_mechanic_repository import MechanicRepositorySQL

from app.utility.db_mongo import get_db as get_mongo_db
from app.utility.db_neo import get_neo
from app.utility.db_sql import get_sql_db


def get_mechanic_repository():
    db_mode = os.getenv("DB_MODE", "sql").lower()

    if db_mode == "sql":
        db = next(get_sql_db())
        return MechanicRepositorySQL(db)

    if db_mode == "mongo":
        db = next(get_mongo_db())
        return MechanicRepositoryMongo(db)

    if db_mode == "neo":
        driver = get_neo()
        return MechanicRepositoryNeo(driver)

    raise ValueError(f"Unknown DB_MODE: {db_mode}")
