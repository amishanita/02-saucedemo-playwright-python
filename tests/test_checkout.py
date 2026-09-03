"""Checkout tests: TC-CHK-001 to TC-CHK-004."""
import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.test_data import get_checkout_info

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.fixture
def checkout_page(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.open_cart()
    CartPage(inventory_page.page).checkout()
    return CheckoutPage(inventory_page.page)


@pytest.mark.checkout
@pytest.mark.positive
@pytest.mark.smoke
def test_chk_001_complete_order_happy_path(checkout_page):
    info = get_checkout_info()
    checkout_page.fill_information(info["first_name"], info["last_name"], info["postal_code"])
    checkout_page.continue_checkout()

    assert CheckoutPage.STEP_TWO_URL_PART in checkout_page.page.url

    checkout_page.finish()

    assert CheckoutPage.COMPLETE_URL_PART in checkout_page.page.url
    expect(checkout_page.complete_header).to_be_visible()
    assert "Thank you for your order" in checkout_page.get_confirmation_text()
    expect(checkout_page.page.locator('[data-test="shopping-cart-badge"]')).not_to_be_visible()


@pytest.mark.checkout
@pytest.mark.negative
@pytest.mark.parametrize(
    "first_name,last_name,postal_code,expected_message",
    [
        ("", "Yamada", "220-0011", "First Name is required"),
        ("Taro", "", "220-0011", "Last Name is required"),
        ("Taro", "Yamada", "", "Postal Code is required"),
    ],
    ids=["missing_first_name", "missing_last_name", "missing_postal_code"],
)
def test_chk_002_required_field_validation(
    checkout_page, first_name, last_name, postal_code, expected_message
):
    checkout_page.fill_information(first_name, last_name, postal_code)
    checkout_page.continue_checkout()

    expect(checkout_page.error_message).to_be_visible()
    assert expected_message in checkout_page.get_error_text()
    assert CheckoutPage.STEP_ONE_URL_PART in checkout_page.page.url


@pytest.mark.checkout
@pytest.mark.positive
def test_chk_003_overview_items_and_totals(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)
    inventory_page.open_cart()

    cart = CartPage(inventory_page.page)
    expected_names = sorted(cart.get_product_names())
    expected_subtotal = round(sum(cart.get_product_prices()), 2)
    cart.checkout()

    checkout = CheckoutPage(inventory_page.page)
    info = get_checkout_info()
    checkout.fill_information(info["first_name"], info["last_name"], info["postal_code"])
    checkout.continue_checkout()

    assert sorted(checkout.get_product_names()) == expected_names
    assert checkout.get_subtotal() == expected_subtotal
    assert checkout.get_tax() > 0
    # The tax rate is not hard-coded, only the arithmetic is checked.
    assert round(checkout.get_subtotal() + checkout.get_tax(), 2) == checkout.get_total()


@pytest.mark.checkout
@pytest.mark.positive
def test_chk_004_cancel_returns_to_cart(checkout_page):
    checkout_page.cancel()

    cart = CartPage(checkout_page.page)
    assert CartPage.URL_PART in cart.page.url
    assert cart.item_count() == 1
    assert cart.get_product_names() == [BACKPACK]
