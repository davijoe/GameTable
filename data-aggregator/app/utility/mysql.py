import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import Base


DB_USER = os.getenv("MYSQL_USER")
DB_PASS = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_SERVER")
DB_PORT = os.getenv("MYSQL_PORT")
DB_NAME = os.getenv("MYSQL_DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    # Import models so they are registered with Base.metadata
    from app.models import (
        game_model,
        artist_model,
        designer_model,
        mechanic_model,
        genre_model,
    )  # noqa

    Base.metadata.create_all(bind=engine)
