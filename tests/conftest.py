import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import schema, models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings
from app.database import get_db
from app.oauth2 import create_access_token
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

@pytest.fixture
def test_user(client):
    user_data = {"email": "alanwang@gmail.com",
                 "password": "password123"}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(test_user, session, client):
    posts_data = [
        models.Post(title="first title", content="first content", owner_id=test_user["id"]),
        models.Post(title="2nd title",   content="2nd content",  owner_id=test_user["id"]),
        models.Post(title="3rd title",   content="3rd content",  owner_id=test_user["id"]),
    ]
    session.add_all(posts_data)
    session.commit()
    # for p in posts_data:
    #     session.refresh(p)

    other_user_data = {"email": "other@example.com", "password": "password123"}
    res = client.post("/users/", json=other_user_data)
    assert res.status_code == 201
    other_user = res.json()

    other_user_post = models.Post(
            title="other user post", content="post from another user", owner_id=other_user["id"]
        )
    session.add(other_user_post)

    session.commit()

    all_posts = posts_data + [other_user_post]
    for p in all_posts:
        session.refresh(p)

    return all_posts