import requests
import pytest
from faker import Faker
from tests.api.conftest import BASE_URL
from tests.api.conftest import user_data, registered_user, auth_session


@pytest.mark.negative
def test_create_user_with_existing_email(user_data):
    """Test creating a user with an existing email."""
    # First create a user
    response = requests.post(f"{BASE_URL}/api/users", json=user_data)
    assert response.status_code == 201

    # Now try to create another user with the same email
    response = requests.post(f"{BASE_URL}/api/users", json=user_data)
    assert response.status_code == 400
    assert "User already exists" in response.text


@pytest.mark.negative
def test_get_token_with_invalid_credentials():
    """Test getting a token with invalid credentials."""
    invalid_credentials = {
        "name": "Test User",
        "email": "asdasd",
        "password": "wrongpassword"}
    response = requests.post(f"{BASE_URL}/api/users/auth", json=invalid_credentials)
    assert response.status_code == 401
    assert "Invalid email or password" in response.text
    
    