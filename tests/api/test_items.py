import requests
import pytest
from faker import Faker

BASE_URL = "http://localhost:3000"

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


@pytest.mark.positive
def test_create_user(user_data):
    """Test creating a new user."""
    json_data= user_data
    response = requests.post(f"{BASE_URL}/api/users", json=json_data)
    assert response.status_code == 201
    assert "_id" in response.json()

@pytest.mark.positive
def test_get_token(registered_user):
    """Test getting a token for the user."""
    response = requests.post(f"{BASE_URL}/api/users/auth", json={
        "email": registered_user["email"],
        "password": registered_user["password"]
    })
    assert response.status_code == 200
    assert "_id" in response.json()  # Or other auth response fields

@pytest.mark.positive
def test_logout(registered_user):
    """Test logging out the user."""
    response = requests.post(f"{BASE_URL}/api/users/logout")
    assert response.status_code == 200
    assert response.json().get("message") == "Logged out successfully"