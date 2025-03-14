import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.main import app, get_db

# Create a test database and session
TEST_DATABASE_URL = (
    "sqlite:///./tests/test.db"  # Use an in-memory SQLite database for testing
)
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session with a rollback at the end of the test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


# Override the get_db dependency to use the testing database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture()
def peak_id() -> str:
    """Generate a random peak id."""
    return str(uuid.uuid4())


# Fixture to generate a user payload
@pytest.fixture()
def peak_payload(peak_id):
    """Generate a peak payload."""
    return {
        "name": "Pic du Midi de Bigorre",
        "lat": 42.936,
        "lng": 0.137,
        "altitude": 2877,
    }


@pytest.fixture()
def peak_payload_updated(peak_id):
    """Generate an updated peak payload."""
    return {
        "name": "Pic du Midi de Bigorre after hearthquake",
        "lat": 43.1,
        "lng": 0.1,
        "altitude": 2650,
    }
