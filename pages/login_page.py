from playwright.sync_api import Page

from utils.test_data import BASE_URL


class LoginPage:

    def __init__(self, page: Page) -> None:
        self.page = page
        self.username_input = page.locator('[data-test="username"]')
        self.password_input = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-button"]')
        self.error_message = page.locator('[data-test="error"]')

    def open(self) -> None:
        self.page.goto(BASE_URL)

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def clear_fields(self) -> None:
        self.username_input.fill("")
        self.password_input.fill("")

    def get_error_text(self) -> str:
        return self.error_message.inner_text()

    def is_error_visible(self) -> bool:
        return self.error_message.is_visible()

    def is_login_button_visible(self) -> bool:
        return self.login_button.is_visible()
