import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import schema, models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings
from app.database import get_db

from alembic import command

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1019@localhost:5432/fastapi_test"
SQLALCHEMY_DATABASE_URL= (
    f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def session():
    models.Base.metadata.drop_all(bind=engine)
    # create table
    models.Base.metadata.create_all(bind=engine)
    # command.upgrade("head")
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# client = TestClient(app)
@pytest.fixture(scope="function")
def client(session):
    # ---- before code run ---
    def override_get_db():
        # try:
        yield session
        # finally:
        #     session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    # ---- before code run ---