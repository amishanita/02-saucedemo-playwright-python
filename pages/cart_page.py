from typing import List

from playwright.sync_api import Page


class CartPage:

    URL_PART = "/cart.html"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.items = page.locator('[data-test="inventory-item"]')
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.item_prices = page.locator('[data-test="inventory-item-price"]')
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.continue_shopping_button = page.locator('[data-test="continue-shopping"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')

    def item_count(self) -> int:
        return self.items.count()

    def is_empty(self) -> bool:
        return self.item_count() == 0

    def get_product_names(self) -> List[str]:
        return self.item_names.all_inner_texts()

    def get_product_prices(self) -> List[float]:
        return [float(t.replace("$", "")) for t in self.item_prices.all_inner_texts()]

    def remove(self, product_name: str) -> None:
        self.items.filter(has_text=product_name).get_by_role("button", name="Remove").click()

    def remove_all_items(self) -> None:
        while self.item_count() > 0:
            self.items.first.get_by_role("button", name="Remove").click()

    def cart_count(self) -> int:
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.inner_text())

    def continue_shopping(self) -> None:
        self.continue_shopping_button.click()

    def checkout(self) -> None:
        self.checkout_button.click()
