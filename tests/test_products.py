"""Product tests: TC-PROD-001 to TC-PROD-006."""
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.product_page import ProductPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.products
@pytest.mark.positive
@pytest.mark.smoke
def test_prod_001_inventory_page_lists_six_products(inventory_page):
    expect(inventory_page.title).to_have_text("Products")
    assert inventory_page.product_count() == 6

    names = inventory_page.get_product_names()
    prices = inventory_page.get_product_prices()

    assert len(names) == 6
    assert len(prices) == 6
    assert all(name.strip() for name in names)
    assert all(price > 0 for price in prices)


@pytest.mark.products
@pytest.mark.positive
@pytest.mark.parametrize(
    "sort_label,field,reverse",
    [
        (InventoryPage.SORT_NAME_ASC, "name", False),
        (InventoryPage.SORT_NAME_DESC, "name", True),
        (InventoryPage.SORT_PRICE_ASC, "price", False),
        (InventoryPage.SORT_PRICE_DESC, "price", True),
    ],
    ids=["name_a_to_z", "name_z_to_a", "price_low_to_high", "price_high_to_low"],
)
def test_prod_002_sorting_orders_products_correctly(inventory_page, sort_label, field, reverse):
    inventory_page.sort_by(sort_label)

    if field == "name":
        actual = inventory_page.get_product_names()
    else:
        actual = inventory_page.get_product_prices()

    assert actual == sorted(actual, reverse=reverse)


@pytest.mark.products
@pytest.mark.positive
@pytest.mark.smoke
def test_prod_003_product_detail_shows_matching_data(inventory_page):
    inventory_page.open_product(BACKPACK)

    product = ProductPage(inventory_page.page)
    expect(product.name).to_be_visible()
    assert product.get_name() == BACKPACK
    assert product.get_description().strip() != ""
    assert product.get_price().startswith("$")


@pytest.mark.products
@pytest.mark.positive
@pytest.mark.smoke
def test_prod_004_add_to_cart_from_inventory_updates_badge(inventory_page):
    assert inventory_page.cart_count() == 0

    inventory_page.add_to_cart(BACKPACK)

    expect(inventory_page.cart_badge).to_have_text("1")
    card = inventory_page.item_card(BACKPACK)
    expect(card.get_by_role("button", name="Remove")).to_be_visible()


@pytest.mark.products
@pytest.mark.positive
def test_prod_005_add_to_cart_from_product_detail(inventory_page):
    inventory_page.open_product(BIKE_LIGHT)

    product = ProductPage(inventory_page.page)
    product.add_to_cart()

    expect(product.cart_badge).to_have_text("1")
    expect(product.page.get_by_role("button", name="Remove")).to_be_visible()


@pytest.mark.products
@pytest.mark.positive
def test_prod_006_remove_from_inventory_clears_badge(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    expect(inventory_page.cart_badge).to_have_text("1")

    inventory_page.remove_from_cart(BACKPACK)

    expect(inventory_page.cart_badge).not_to_be_visible()
    card = inventory_page.item_card(BACKPACK)
    expect(card.get_by_role("button", name="Add to cart")).to_be_visible()
