import pytest
import requests
from faker import Faker


BASE_URL = "http://localhost:5000"


@pytest.fixture
def fake():
    return Faker()


@pytest.fixture
def user_data(fake):
    return {
        "name": fake.name(),
        "email": fake.email(),
        "password": fake.password()
    }


@pytest.fixture
def registered_user(user_data):
    """register a user and return their credentials."""
    response = requests.post(f"{BASE_URL}/api/users", json=user_data)
    assert response.status_code == 201
    return user_data


@pytest.fixture
def auth_session(registered_user):
    """Log in user and return authenticated session."""
    session = requests.Session()
    login_response = session.post(f"{BASE_URL}/api/users/auth", json={
        "email": registered_user["email"],
        "password": registered_user["password"]
    })
    assert login_response.status_code == 200
    return session  # this session has the jwt cookie set
