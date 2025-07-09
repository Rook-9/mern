import pytest
import requests
from faker import Faker

@pytest.fixture
def fake_user_correct():
    """Fixture to create a fake user with correct credentials."""
    fake = Faker()
    return {
        "name": fake.name(),
        "email": fake.email(),
        "password": fake.password()
    }

@pytest.fixture
def exist_user():
    """Credentials of already registered user."""
    return{
            "name": "test",
            "email": "test@gmail.com",
            "password": "1234"
        }

@pytest.fixture
def base_url():
    """Base URL for the API."""
    return "http://localhost:3000"