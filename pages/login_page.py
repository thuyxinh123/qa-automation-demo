from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com"


class LoginPage:
    """Page Object cho màn hình đăng nhập."""

    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("[data-test='username']")
        self.password = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-button']")
        self.error_message = page.locator("[data-test='error']")

    def open(self):
        self.page.goto(BASE_URL)

    def login(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()

    def expect_error(self, text: str):
        expect(self.error_message).to_contain_text(text)
