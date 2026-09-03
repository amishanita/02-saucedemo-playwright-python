from playwright.sync_api import Page


class ProductPage:

    def __init__(self, page: Page) -> None:
        self.page = page
        self.name = page.locator('[data-test="inventory-item-name"]')
        self.description = page.locator('[data-test="inventory-item-desc"]')
        self.price = page.locator('[data-test="inventory-item-price"]')
        self.back_button = page.locator('[data-test="back-to-products"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')

    def get_name(self) -> str:
        return self.name.inner_text()

    def get_description(self) -> str:
        return self.description.inner_text()

    def get_price(self) -> str:
        return self.price.inner_text()

    def add_to_cart(self) -> None:
        self.page.get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self) -> None:
        self.page.get_by_role("button", name="Remove").click()

    def cart_count(self) -> int:
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.inner_text())

    def back_to_products(self) -> None:
        self.back_button.click()
