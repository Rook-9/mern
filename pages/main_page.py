from playwright.sync_api import Page, expect
import re

class MainPage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto("http://localhost:3000/")

    def assert_user_info(self, name: str):
        self.page.get_by_role("button", name=name)

    def logout(self, name: str):
        self.page.get_by_role("button", name=name).click()
        self.page.get_by_role("button", name="Logout").click()
        expect(self.page).to_have_url(re.compile(r"http://localhost:3000/login"))