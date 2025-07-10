from playwright.sync_api import Page, expect
import re

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto("http://localhost:3000/login")

    def login(self, email: str, password: str):
        self.page.fill('input[id="email"]', email)
        self.page.fill('input[id="password"]', password)
        self.page.click('button:has-text("Sign In")')

    def assert_logged_in(self):
        expect(self.page).to_have_url(re.compile(r"http://localhost:3000/"))

    def logout(self, name: str):
        self.page.get_by_role("button", name=name).click()
        self.page.get_by_role("button", name="Logout").click()
        expect(self.page).to_have_url(re.compile(r"http://localhost:3000/login"))
