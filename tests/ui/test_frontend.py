import re
import pytest
from faker import Faker
from playwright.sync_api import Page, expect, sync_playwright
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from tests.ui.conftest import exist_user

@pytest.mark.ui
@pytest.mark.positive
def test_frontend_register(page: Page):
    """Test the registration functionality on the frontend."""
    register_page = RegisterPage(page)

    name = Faker().name()
    email = Faker().email()
    password = Faker().password()

    register_page.goto()
    register_page.fill_form(name, email, password)
    register_page.submit()
    register_page.assert_redirected_to_home()
    register_page.logout(name)


@pytest.mark.ui
@pytest.mark.positive
def test_frontend_login(page: Page, exist_user):
    """Test the login functionality on the frontend."""
    login_page = LoginPage(page)
    main_page = MainPage(page)
    
    email = exist_user["email"]
    password = exist_user["password"]
    username = exist_user["name"]

    # Fill in the login form
    login_page.goto()
    login_page.login(email, password)
    # Check if the user is redirected to the home page
    login_page.assert_logged_in()
    # Wait for the response and check if the user is redirected to the home page
    expect(page).to_have_url(re.compile(r"http://localhost:3000/"))
    main_page.logout(username)
    # Check if the user is logged out
    expect(page).to_have_url(re.compile(r"http://localhost:3000/login"))


@pytest.mark.ui
@pytest.mark.negative
def test_frontend_register_existing_user(page: Page):
    """Test the login functionality on the frontend with invalid credentials."""
    register_page = RegisterPage(page)
    register_page.goto()
    register_page.fill_form("test", "test@gmail.com", "1234")
    register_page.submit()
    # Check if the error message is displayed
    register_page.alert_message()