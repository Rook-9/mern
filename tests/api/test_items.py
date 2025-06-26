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


def test_create_user(user_data):
    """Test creating a new user."""
    json_data= user_data
    response = requests.post(f"{BASE_URL}/api/users", json=json_data)
    assert response.status_code == 201
    assert "_id" in response.json()