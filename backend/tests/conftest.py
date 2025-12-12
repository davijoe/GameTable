import os  # BEFORE app.main and app.utility.*

os.environ["DATABASE_URL"] = "sqlite:///./test.db"  # noqa: F821


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.utility.auth import get_current_user, require_admin
from app.utility.db_sql import Base, get_sql_db

TEST_DB_URL = "sqlite:///./test.db"


engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="session", autouse=True)
def create_test_schema():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def override_db(db_session):
    def _get_db():
        yield db_session

    app.dependency_overrides[get_sql_db] = _get_db
    yield
    app.dependency_overrides.pop(get_sql_db, None)


@pytest.fixture(autouse=True)
def override_user():
    def fake_user():
        return {"id": "test-user", "role": "admin"}

    app.dependency_overrides[get_current_user] = fake_user
    yield
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def override_require_admin():
    """Override require_admin"""

    def allow_admin():
        return True

    app.dependency_overrides[require_admin] = allow_admin
    yield
    app.dependency_overrides.pop(require_admin, None)
