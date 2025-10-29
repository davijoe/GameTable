import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

print(f"User: {DB_USER} | Pass: {DB_PASS}")
print(f"Host: {DB_HOST} | Port: {DB_PORT}")
print(f"Database: {DB_NAME}")

# Example:
# export DATABASE_URL="mysql+pymysql://user:pass@localhost:3306/gametable"
DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql+pymysql://appuser:change_me_too@localhost:3306/gametable"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
