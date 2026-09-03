"""Cart tests: TC-CART-001 to TC-CART-005."""
import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.cart
@pytest.mark.positive
@pytest.mark.smoke
def test_cart_001_added_product_appears_with_correct_data(inventory_page):
    # Read the price from the product list first so the test still works
    # if the catalogue prices change.
    names = inventory_page.get_product_names()
    prices = inventory_page.get_product_prices()
    expected_price = prices[names.index(BACKPACK)]

    inventory_page.add_to_cart(BACKPACK)
    inventory_page.open_cart()

    cart = CartPage(inventory_page.page)
    assert cart.item_count() == 1
    assert cart.get_product_names() == [BACKPACK]
    assert cart.get_product_prices() == [expected_price]


@pytest.mark.cart
@pytest.mark.positive
def test_cart_002_badge_matches_number_of_items(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)

    expect(inventory_page.cart_badge).to_have_text("2")

    inventory_page.open_cart()
    cart = CartPage(inventory_page.page)
    assert cart.item_count() == 2
    assert sorted(cart.get_product_names()) == sorted([BACKPACK, BIKE_LIGHT])


@pytest.mark.cart
@pytest.mark.positive
@pytest.mark.smoke
def test_cart_003_remove_from_cart_empties_it(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.open_cart()

    cart = CartPage(inventory_page.page)
    cart.remove(BACKPACK)

    assert cart.item_count() == 0
    expect(cart.cart_badge).not_to_be_visible()


@pytest.mark.cart
@pytest.mark.positive
def test_cart_004_continue_shopping_returns_to_inventory(inventory_page):
    inventory_page.open_cart()

    cart = CartPage(inventory_page.page)
    cart.continue_shopping()

    assert InventoryPage.URL_PART in cart.page.url
    expect(inventory_page.title).to_have_text("Products")


@pytest.mark.cart
@pytest.mark.positive
def test_cart_005_cart_survives_navigation(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.open_cart()

    cart = CartPage(inventory_page.page)
    cart.continue_shopping()
    inventory_page.open_cart()

    assert cart.item_count() == 1
    assert cart.get_product_names() == [BACKPACK]
    expect(cart.cart_badge).to_have_text("1")
