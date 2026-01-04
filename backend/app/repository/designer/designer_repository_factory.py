import os

from app.repository.designer.designer_repository_mongo import DesignerRepositoryMongo
from app.repository.designer.designer_repository_neo import DesignerRepositoryNeo
from app.repository.designer.sql_designer_repository import SQLDesignerRepository
from app.utility.db_mongo import get_db as get_mongo_db
from app.utility.db_neo import get_neo
from app.utility.db_sql import get_sql_db

DB_MODE = os.getenv("DB_MODE", "sql").lower()


def get_designer_repository():
    if DB_MODE == "sql":
        db = next(get_sql_db())
        return SQLDesignerRepository(db)
    elif DB_MODE == "mongo":
        db = next(get_mongo_db())
        return DesignerRepositoryMongo(db)
    elif DB_MODE == "neo":
        db = get_neo()
        return DesignerRepositoryNeo(db)

    raise ValueError(f"Unknown DB_MODE: {DB_MODE}")
