import re
import pytest
from faker import Faker
from playwright.sync_api import Page, expect, sync_playwright
from tests.ui.conftest import exist_user

@pytest.mark.ui
@pytest.mark.positive
def test_frontend_register(page: Page):
    """Test the login functionality on the frontend."""
    page.goto("http://localhost:3000/register")
    
    password = Faker().password()
    username = Faker().name()
    # Fill in the login form
    page.fill('input[id="name"]', username)
    page.fill('input[id="email"]', Faker().email())
    page.fill('input[id="password"]', password) 
    page.fill('input[id="confirmPassword"]', password)
    page.click('button:has-text("Register")')

    # Wait for the response and check if the user is redirected to the home page
    expect(page).to_have_url(re.compile(r"http://localhost:3000/"))
    page.get_by_role("button", name=username).click()
    page.get_by_role("button", name="Logout").click()
    # Check if the user is logged out
    expect(page).to_have_url(re.compile(r"http://localhost:3000/login"))


@pytest.mark.ui
@pytest.mark.positive
def test_frontend_login(page: Page, exist_user):
    """Test the login functionality on the frontend."""
    page.goto("http://localhost:3000/login")
    
    email = exist_user["email"]
    password = exist_user["password"]
    username = exist_user["name"]
    
    # Fill in the login form
    page.fill('input[id="email"]', email)
    page.fill('input[id="password"]', password)
    page.click('button:has-text("Sign In")')

    # Wait for the response and check if the user is redirected to the home page
    expect(page).to_have_url(re.compile(r"http://localhost:3000/"))
    page.get_by_role("button", name=username).click()
    page.get_by_role("button", name="Logout").click()
    # Check if the user is logged out
    expect(page).to_have_url(re.compile(r"http://localhost:3000/login"))