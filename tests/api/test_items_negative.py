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
    

@pytest.mark.negative
def test_get_user_without_auth(auth_session):
    """Test getting user details without authentication."""
    # Clear the session to simulate no auth
    auth_session.cookies.clear()
    
    response = auth_session.get(f"{BASE_URL}/api/users/profile")
    assert response.status_code == 401
    assert "Not authorized, no token" in response.text


@pytest.mark.negative
def test_update_user_without_auth(auth_session, registered_user):
    """Test updating user details without authentication."""
    # Clear the session to simulate no auth
    auth_session.cookies.clear()
    
    updated_data = {
        "name": "New Name",
        "email": "newtestemail@gmail.com"}
    response = auth_session.put(f"{BASE_URL}/api/users/profile", json=updated_data)
    assert response.status_code == 401
    assert "Not authorized, no token" in response.text  


@pytest.mark.xfail(reason="Logout validation functionality is not implemented yet")
@pytest.mark.negative
def test_logout_without_auth(auth_session):
    """Test logging out without authentication."""
    auth_session.cookies.clear()

    response = requests.post(f"{BASE_URL}/api/users/logout")
    assert response.status_code == 401
    assert "Not authorized, no token" in response.text


@pytest.mark.xfail(reason="User email validation functionality is not implemented yet")
@pytest.mark.negative
def test_create_user_with_invalid_email():
    """Test creating a user with an invalid email format."""
    invalid_email = f"{Faker().uuid4()}-bademail"
    json_data = {
        "name": Faker().name(),
        "email": invalid_email,  # Invalid email
        "password": Faker().password()
    }

    response = requests.post(f"{BASE_URL}/api/users", json=json_data)
    # Expecting a 400 Bad Request due to invalid email format
    assert response.status_code == 401
    assert "Invalid email format" in response.text

@pytest.mark.xfail(reason="User password validation functionality is not implemented yet")
@pytest.mark.negative
def test_create_user_with_missing_email():
    """Test creating a user with missing required fields."""
    json_data = {
        "name": Faker().name(),
        "email": "",  # Missing email
        "password": Faker().password()  # Valid password
    }

    response = requests.post(f"{BASE_URL}/api/users", json=json_data)
    assert response.status_code == 400
    assert "Missing required fields" in response.text


@pytest.mark.xfail(reason="User password validation functionality is not implemented yet")
@pytest.mark.negative
def test_create_user_with_missing_password():
    """Test creating a user with missing password."""
    json_data = {
        "name": Faker().name(),
        "email": Faker().email(),  # Valid email
        "password": ""  # Missing password
    }

    response = requests.post(f"{BASE_URL}/api/users", json=json_data)
    assert response.status_code == 400
    assert "Missing required fields" in response.text