from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings import settings

from app.model.base import Base

DB_USER = settings.mysql_user
DB_PASS = settings.mysql_password
DB_HOST = settings.mysql_server
DB_PORT = settings.mysql_port
DB_NAME = settings.mysql_db_name

print(f"User:{DB_USER} | host:{DB_HOST} | port:{DB_PORT} | name:{DB_NAME}")

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
