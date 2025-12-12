import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.utility.db_sql import Base, get_sql_db

DB_USER = os.getenv("MYSQL_TEST_USER")
DB_PASS = os.getenv("MYSQL_TEST_PASSWORD")
DB_HOST = os.getenv("MYSQL_TEST_SERVER")
DB_PORT = os.getenv("MYSQL_TEST_PORT")
DB_NAME = os.getenv("MYSQL_TEST_DB_NAME")

TEST_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    os.environ["DB_MODE"] = "test"

    # Create tables for all models
    Base.metadata.create_all(bind=engine)
    yield
    # And drop them after tests
    Base.metadata.drop_all(bind=engine)


def override_get_sql_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def test_app(setup_test_db):  # noqa: ARG001
    app.dependency_overrides[get_sql_db] = override_get_sql_db
    yield app
    app.dependency_overrides.clear()


@pytest.fixture
def client(test_app):
    with TestClient(test_app) as c:
        yield c
