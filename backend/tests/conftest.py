import os  # BEFORE app.main and app.utility.*
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///./test.db"  # noqa: F821


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.utility.auth import get_current_user, require_admin
from app.utility.db_sql import Base, get_sql_db

TEST_DB_URL = os.environ["DATABASE_URL"]

UNIT = "unit"
INTEGRATION = "integration"
REQUIRED_MARKERS = {UNIT, INTEGRATION}

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


@pytest.fixture
def _allow_admin():
    def _allow():
        return True

    app.dependency_overrides[require_admin] = _allow
    yield
    app.dependency_overrides.pop(require_admin, None)


@pytest.fixture
def _deny_admin():
    from fastapi import HTTPException

    def _deny():
        raise HTTPException(status_code=403, detail="Not enough permissions")

    app.dependency_overrides[require_admin] = _deny
    yield
    app.dependency_overrides.pop(require_admin, None)

#applies a isUnit or isIntegration marker for every test based on the folder structure
#run unit with:     uv run pytest -m integration
#run integration:   uv run pytest -m unit
#run both:          uv run pytest
def pytest_collection_modifyitems(items):
    for item in items:
        path = Path(item.fspath).as_posix()

        is_unit = f"/{UNIT}/" in path
        is_integration = f"/{INTEGRATION}/" in path

        has_unit = item.get_closest_marker(UNIT)
        has_integration = item.get_closest_marker(INTEGRATION)

        # Folder → marker
        if is_unit:
            if has_integration:
                pytest.fail(f"{item.nodeid} is in /unit/ but marked integration")
            item.add_marker(pytest.mark.unit)

        elif is_integration:
            if has_unit:
                pytest.fail(f"{item.nodeid} is in /integration/ but marked unit")
            item.add_marker(pytest.mark.integration)

        # Safety net
        if not (has_unit or has_integration or is_unit or is_integration):
            pytest.fail(
                f"{item.nodeid} must live in /unit/ or /integration/ "
                f"or be explicitly marked"
            )
