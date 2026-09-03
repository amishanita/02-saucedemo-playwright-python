import pytest
from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.test_data import get_product_name, get_user

# pytest-playwright already gives every test a fresh browser context, so
# the cart starts empty and nothing leaks between tests. No extra
# storage-clearing fixture is needed.


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    lp = LoginPage(page)
    lp.open()
    return lp


@pytest.fixture
def inventory_page(login_page: LoginPage) -> InventoryPage:
    user = get_user("valid")
    login_page.login(user["username"], user["password"])
    return InventoryPage(login_page.page)


@pytest.fixture
def cart_with_one_item(inventory_page: InventoryPage) -> CartPage:
    inventory_page.add_to_cart(get_product_name("backpack"))
    inventory_page.open_cart()
    return CartPage(inventory_page.page)


@pytest.fixture
def cart_with_two_items(inventory_page: InventoryPage) -> CartPage:
    inventory_page.add_to_cart(get_product_name("backpack"))
    inventory_page.add_to_cart(get_product_name("bike_light"))
    inventory_page.open_cart()
    return CartPage(inventory_page.page)
