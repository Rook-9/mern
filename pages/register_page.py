from playwright.sync_api import Page, expect
import re

class RegisterPage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto("http://localhost:3000/register")

    def fill_form(self, name: str, email: str, password: str):
        self.page.fill('input[id="name"]', name)
        self.page.fill('input[id="email"]', email)
        self.page.fill('input[id="password"]', password)
        self.page.fill('input[id="confirmPassword"]', password)

    def submit(self):
        self.page.click('button:has-text("Register")')

    def assert_redirected_to_home(self):
        expect(self.page).to_have_url(re.compile(r"http://localhost:3000/"))

    def logout(self, name: str):
        self.page.get_by_role("button", name=name).click()
        self.page.get_by_role("button", name="Logout").click()
        expect(self.page).to_have_url(re.compile(r"http://localhost:3000/login"))

    def alert_message(self):
        """Check if the alert message is visible."""
        expect(self.page.get_by_role("alert")).to_be_visible()
