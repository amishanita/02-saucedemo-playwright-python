"""Login tests: TC-LOGIN-001 to TC-LOGIN-007."""
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from utils.test_data import BASE_URL, get_user


@pytest.mark.login
@pytest.mark.positive
@pytest.mark.smoke
def test_login_001_valid_login_redirects_to_inventory(login_page):
    user = get_user("valid")
    login_page.login(user["username"], user["password"])

    inventory = InventoryPage(login_page.page)
    expect(login_page.page).to_have_url(BASE_URL.rstrip("/") + InventoryPage.URL_PART)
    expect(inventory.title).to_have_text("Products")
    assert inventory.product_count() == 6


@pytest.mark.login
@pytest.mark.negative
def test_login_002_invalid_username_is_rejected(login_page):
    user = get_user("invalid_username")
    login_page.login(user["username"], user["password"])

    expect(login_page.error_message).to_be_visible()
    assert "do not match any user in this service" in login_page.get_error_text()
    assert InventoryPage.URL_PART not in login_page.page.url


@pytest.mark.login
@pytest.mark.negative
def test_login_003_invalid_password_is_rejected(login_page):
    # SauceDemo shows the same message as a wrong username, so the
    # assertion checks the shared text rather than a password-specific one.
    user = get_user("invalid_password")
    login_page.login(user["username"], user["password"])

    expect(login_page.error_message).to_be_visible()
    assert "do not match any user in this service" in login_page.get_error_text()
    assert InventoryPage.URL_PART not in login_page.page.url


@pytest.mark.login
@pytest.mark.negative
@pytest.mark.parametrize(
    "username,password,expected_message",
    [
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
        ("", "", "Username is required"),
    ],
    ids=["empty_username", "empty_password", "both_empty"],
)
def test_login_004_required_field_validation(login_page, username, password, expected_message):
    login_page.login(username, password)

    expect(login_page.error_message).to_be_visible()
    assert expected_message in login_page.get_error_text()


@pytest.mark.login
@pytest.mark.negative
def test_login_005_locked_out_user_is_blocked(login_page):
    user = get_user("locked_out")
    login_page.login(user["username"], user["password"])

    expect(login_page.error_message).to_be_visible()
    assert "locked out" in login_page.get_error_text()
    assert InventoryPage.URL_PART not in login_page.page.url


@pytest.mark.login
@pytest.mark.positive
def test_login_006_logout_returns_to_login_page(inventory_page):
    inventory_page.logout()

    expect(inventory_page.page.locator('[data-test="login-button"]')).to_be_visible()
    assert InventoryPage.URL_PART not in inventory_page.page.url


@pytest.mark.login
@pytest.mark.negative
def test_login_007_direct_url_access_without_login_is_blocked(page):
    page.goto(BASE_URL.rstrip("/") + InventoryPage.URL_PART)

    expect(page.locator('[data-test="error"]')).to_be_visible()
    expect(page.locator('[data-test="login-button"]')).to_be_visible()


@pytest.mark.login
@pytest.mark.skip(reason="problem_user shows broken images; needs image comparison, which is out of scope")
def test_login_008_problem_user_visual_issues(login_page):
    raise NotImplementedError


@pytest.mark.login
@pytest.mark.slow
def test_login_009_performance_glitch_user_can_still_log_in(login_page):
    """This user is deliberately slow. The test has no explicit wait,
    because expect() keeps retrying until the page appears."""
    user = get_user("performance_glitch")
    login_page.login(user["username"], user["password"])

    inventory = InventoryPage(login_page.page)
    expect(inventory.title).to_have_text("Products", timeout=30000)
    assert inventory.product_count() == 6
