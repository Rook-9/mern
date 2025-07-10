import requests
import pytest
from faker import Faker
from tests.api.conftest import BASE_URL
from tests.api.conftest import user_data, registered_user, auth_session, cleanup_user


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
def test_get_user(auth_session, registered_user):
    """Test getting the user details."""
    response = auth_session.get(f"{BASE_URL}/api/users/profile")
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == registered_user["email"]
    assert user_data["name"] == registered_user["name"]


@pytest.mark.positive
def test_update_user(auth_session, registered_user, fake):
    """Test updating the user details."""
    updated_data = {
        "name": fake.name(),
        "email": fake.email(),
        "password": registered_user["password"]  # keep the same password
    }
    response = auth_session.put(f"{BASE_URL}/api/users/profile", json=updated_data)
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == updated_data["email"]
    assert user_data["name"] == updated_data["name"]


@pytest.mark.positive
def test_logout(registered_user):
    """Test logging out the user."""
    response = requests.post(f"{BASE_URL}/api/users/logout")
    assert response.status_code == 200
    assert response.json().get("message") == "Logged out successfully"


@pytest.mark.positive
def test_get_all_users(auth_session):
    """Test getting all users."""
    response = auth_session.get(f"{BASE_URL}/api/users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) > 0
    for user in users:
        assert "email" in user
        assert "name" in user
        assert "_id" in user

@pytest.mark.positive
def test_delete_user(auth_session, registered_user):
    """Test deleting the user."""
    response = auth_session.delete(f"{BASE_URL}/api/users/profile")
    assert response.status_code == 200
    assert response.json().get("message") == "User deleted successfully"

    # Verify the user is no longer retrievable
    response = auth_session.get(f"{BASE_URL}/api/users/profile")
    assert response.status_code == 401
    assert "Not authorized, token failed" in response.text
