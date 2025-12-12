import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


def get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if url:
        return url

    user = os.getenv("MYSQL_USER")
    pw = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("MYSQL_SERVER")
    port = os.getenv("MYSQL_PORT")
    name = os.getenv("MYSQL_DB_NAME")

    if not all([user, pw, host, name]):
        missing = [
            k
            for k, v in {
                "MYSQL_USER": user,
                "MYSQL_PASSWORD": pw,
                "MYSQL_SERVER": host,
                "MYSQL_DB_NAME": name,
            }.items()
            if not v
        ]
        raise RuntimeError(f"Missing DB env vars: {', '.join(missing)}")

    if port:
        return f"mysql+pymysql://{user}:{pw}@{host}:{port}/{name}"
    return f"mysql+pymysql://{user}:{pw}@{host}/{name}"


DATABASE_URL = get_database_url()


engine_kwargs = {"pool_pre_ping": True, "future": True}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_kwargs)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


class Base(DeclarativeBase):
    pass


def get_sql_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
