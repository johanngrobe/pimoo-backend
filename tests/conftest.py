from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.main import app

from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


# @pytest.fixture
# def test_user2(client):
#     user_data = {"email": "sanjeev123@gmail.com",
#                  "password": "password123"}
#     res = client.post("/users/", json=user_data)

#     assert res.status_code == 201

#     new_user = res.json()
#     new_user['password'] = user_data['password']
#     return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", 
                 "password": "password123",
                 "first_name": "hello",
                 "last_name": "world",
                 "organization": "hello world",
                 "street": "hello",
                 "house_number": "123",
                 "postal_code": "12345",
                 "city": "hello",
                 "country": "world"}

    res = client.post("/user/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_real_estate_mainz(session):
    real_estate_data = [
    {
        "geom": "POINT(50.000205993652344 8.26205825805664)",
        "full_address": "Binger Straße 2, 55116 Mainz",
        "street": "Binger Straße",
        "house_number": "2",
        "postal_code": "",
        "city": "Mainz"
    },
        {
        "geom": "POINT(49.984554 8.249938)",
        "full_address": "Michael-Müller-Ring 23, 55128 Mainz",
        "street": "Michael-Müller-Ring",
        "house_number": "23",
        "postal_code": "55128",
        "city": "Mainz"
    }, {
        "geom": "POINT(49.960860 8.253250)",
        "full_address": "Carl-Zeiss-Straße 42, 55129 Mainz",
        "street": "Carl-Zeiss-Straße",
        "house_number": "42",
        "postal_code": "55129",
        "city": "Mainz"
    }]

    def create_real_estate_model(real_estate):
        return models.RealEstate(**real_estate)

    real_estate_map = map(create_real_estate_model, real_estate_data)
    real_estates = list(real_estate_map)

    session.add_all(real_estates)
    session.commit()

    posts = session.query(models.RealEstate).all()
    return posts