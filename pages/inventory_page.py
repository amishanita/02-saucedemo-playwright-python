from typing import List

from playwright.sync_api import Locator, Page


class InventoryPage:

    URL_PART = "/inventory.html"

    SORT_NAME_ASC = "Name (A to Z)"
    SORT_NAME_DESC = "Name (Z to A)"
    SORT_PRICE_ASC = "Price (low to high)"
    SORT_PRICE_DESC = "Price (high to low)"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.locator('[data-test="title"]')
        self.items = page.locator('[data-test="inventory-item"]')
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.item_prices = page.locator('[data-test="inventory-item-price"]')
        self.sort_dropdown = page.get_by_role("combobox")
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")
        self.reset_link = page.locator("#reset_sidebar_link")

    def item_card(self, product_name: str) -> Locator:
        return self.items.filter(has_text=product_name)

    def product_count(self) -> int:
        return self.items.count()

    def get_product_names(self) -> List[str]:
        return self.item_names.all_inner_texts()

    def get_product_prices(self) -> List[float]:
        return [float(t.replace("$", "")) for t in self.item_prices.all_inner_texts()]

    def sort_by(self, option_label: str) -> None:
        self.sort_dropdown.select_option(label=option_label)

    def add_to_cart(self, product_name: str) -> None:
        self.item_card(product_name).get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self, product_name: str) -> None:
        self.item_card(product_name).get_by_role("button", name="Remove").click()

    def cart_count(self) -> int:
        # The badge element is removed when the cart is empty, so a
        # missing badge means zero.
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.inner_text())

    def open_cart(self) -> None:
        self.cart_link.click()

    def open_product(self, product_name: str) -> None:
        self.item_names.filter(has_text=product_name).click()

    def logout(self) -> None:
        self.menu_button.click()
        self.logout_link.click()

    def reset_app_state(self) -> None:
        self.menu_button.click()
        self.reset_link.click()
