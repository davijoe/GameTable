import os

from app.repository.video.mongo_video_repository import VideoRepositoryMongo
from app.repository.video.neo_video_repository import VideoRepositoryNeo
from app.repository.video.sql_video_repository import VideoRepositorySQL
from app.utility.db_mongo import get_db as get_mongo_db
from app.utility.db_neo import get_neo
from app.utility.db_sql import get_sql_db


def get_video_repository():
    db_mode = os.getenv("DB_MODE", "sql").lower()

    if db_mode == "sql":
        db = next(get_sql_db())
        return VideoRepositorySQL(db)
    if db_mode == "mongo":
        db = next(get_mongo_db())
        return VideoRepositoryMongo(db)
    if db_mode == "neo":
        driver = get_neo()
        return VideoRepositoryNeo(driver)

    raise ValueError(f"Unknown DB_MODE: {db_mode}")
