import os
import pytest
from datetime import datetime, timedelta

from jose import jwt
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

from sqlalchemy_utils import database_exists, create_database, drop_database
from fastapi.testclient import TestClient
from auth.main import app, get_database_url, create_access_token, SECRET_KEY, ALGORITHM
from dotenv import load_dotenv

load_dotenv()

metadata = MetaData()
user_table = Table('user', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('email', String(255), unique=True),
                   Column('password', String(255)))


@pytest.fixture(scope="session")
def test_create_database():
    test_database_url = get_database_url(os.environ['MYSQL_USER'], os.environ['MYSQL_PASSWORD'],
                                         os.environ['MYSQL_HOST'], os.environ['MYSQL_PORT'], 'test_auth')
    engine = create_engine(test_database_url)
    if database_exists(engine.url):
        drop_database(engine.url)
    if not database_exists(engine.url):
        create_database(engine.url)

    metadata.create_all(engine)  # Create tables in the test database

    with engine.connect() as conn:
        # Inserting the test data
        conn.execute(user_table.insert(), [{"email": "alice@email.com", "password": "Admin!23"}])
        # check if the data is inserted
        result = conn.execute(user_table.select()).fetchall()
        conn.commit()

        yield engine

    drop_database(engine.url)  # Cleanup the test database after tests are done


@pytest.fixture(scope="module")
def client(test_create_database):
    with TestClient(app) as client:
        yield client


def test_validate_test_database_state(test_create_database):
    # Connect to the test database
    with test_create_database.connect() as conn:
        # Query the user table
        result = conn.execute(user_table.select()).fetchall()

        # Check if the result contains the expected data
        assert len(result) == 1  # Assuming only one entry is inserted
        user = result[0]
        assert user.email == "alice@email.com"
        assert user.password == "Admin!23"


def get_access_token(client, username, password):
    response = client.post(
        "/token",
        data={"username": username, "password": password},
    )
    return response.json()["access_token"]


def test_token_generation(client, test_create_database):
    response = client.post(
        "/token",
        data={"username": "alice", "password": "Admin!23"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_incorrect_credentials(client, test_create_database):
    # test functionality with incorrect credentials not over rest api

    response = client.post(
        "/token",
        data={"username": "alice", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_read_current_user(client, test_create_database):
    token = get_access_token(client, "alice", "Admin!23")
    response = client.get(
        "/users/me/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"


def test_create_access_token():
    test_data = {"sub": "testuser"}
    token = create_access_token(test_data)
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded_data["sub"] == "testuser"
    assert "exp" in decoded_data
    expected_expiration = datetime.utcnow() + timedelta(minutes=15)
    token_expiration = datetime.utcfromtimestamp(decoded_data["exp"])
    assert token_expiration <= expected_expiration


def test_create_access_token_with_custom_expiration():
    test_data = {"sub": "testuser"}
    custom_expires_delta = timedelta(minutes=30)
    token = create_access_token(test_data, expires_delta=custom_expires_delta)
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    expected_expiration = datetime.utcnow() + custom_expires_delta
    token_expiration = datetime.utcfromtimestamp(decoded_data["exp"])
    assert token_expiration <= expected_expiration


def tests_get_database_url():
    database_url = get_database_url("user", "password", "host", "port", "dbname")
    expected_url = "mysql://user:password@host:port/dbname"
    assert expected_url == database_url
