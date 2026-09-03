from typing import List

from playwright.sync_api import Page


class CheckoutPage:
    """Covers all three checkout steps: information, overview, complete."""

    STEP_ONE_URL_PART = "/checkout-step-one.html"
    STEP_TWO_URL_PART = "/checkout-step-two.html"
    COMPLETE_URL_PART = "/checkout-complete.html"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.first_name_input = page.locator('[data-test="firstName"]')
        self.last_name_input = page.locator('[data-test="lastName"]')
        self.postal_code_input = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.cancel_button = page.locator('[data-test="cancel"]')
        self.error_message = page.locator('[data-test="error"]')
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.item_prices = page.locator('[data-test="inventory-item-price"]')
        self.subtotal_label = page.locator('[data-test="subtotal-label"]')
        self.tax_label = page.locator('[data-test="tax-label"]')
        self.total_label = page.locator('[data-test="total-label"]')
        self.finish_button = page.locator('[data-test="finish"]')
        self.complete_header = page.locator('[data-test="complete-header"]')
        self.back_home_button = page.locator('[data-test="back-to-products"]')

    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def continue_checkout(self) -> None:
        self.continue_button.click()

    def cancel(self) -> None:
        self.cancel_button.click()

    def finish(self) -> None:
        self.finish_button.click()

    def back_home(self) -> None:
        self.back_home_button.click()

    def get_error_text(self) -> str:
        return self.error_message.inner_text()

    def get_product_names(self) -> List[str]:
        return self.item_names.all_inner_texts()

    def get_product_prices(self) -> List[float]:
        return [float(t.replace("$", "")) for t in self.item_prices.all_inner_texts()]

    @staticmethod
    def money(label_text: str) -> float:
        # "Item total: $39.98" -> 39.98
        return float(label_text.split("$")[1])

    def get_subtotal(self) -> float:
        return self.money(self.subtotal_label.inner_text())

    def get_tax(self) -> float:
        return self.money(self.tax_label.inner_text())

    def get_total(self) -> float:
        return self.money(self.total_label.inner_text())

    def get_confirmation_text(self) -> str:
        return self.complete_header.inner_text()
