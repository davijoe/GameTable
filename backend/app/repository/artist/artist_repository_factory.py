import os

from app.repository.artist.artist_repository_mongo import ArtistRepositoryMongo
from app.repository.artist.artist_repository_neo import ArtistRepositoryNeo
from app.repository.artist.sql_artist_repository import ArtistRepositorySQL
from app.utility.db_mongo import get_db as get_mongo_db
from app.utility.db_neo import get_neo
from app.utility.db_sql import get_sql_db

DB_MODE = os.getenv("DB_MODE", "sql").lower()


def get_artist_repository():
    if DB_MODE == "sql":
        db = next(get_sql_db())
        return ArtistRepositorySQL(db)
    elif DB_MODE == "mongo":
        db = next(get_mongo_db())
        return ArtistRepositoryMongo(db)
    elif DB_MODE == "neo":
        db = get_neo()
        return ArtistRepositoryNeo(db)

    raise ValueError(f"Unknown DB_MODE: {DB_MODE}")
