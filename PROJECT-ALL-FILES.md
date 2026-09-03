# SauceDemo Playwright + Python UI Automation

Every file in one document. Each header is the file path.

Status: not run yet / 未実施

31 tests collected. Execution results will be added after the suite is run.

## Files

- `.gitignore`
- `requirements.txt`
- `pytest.ini`
- `conftest.py`
- `utils/test_data.py`
- `test-data/users.json`
- `pages/login_page.py`
- `pages/inventory_page.py`
- `pages/product_page.py`
- `pages/cart_page.py`
- `pages/checkout_page.py`
- `tests/test_login.py`
- `tests/test_products.py`
- `tests/test_cart.py`
- `tests/test_checkout.py`
- `docs/test-cases.md`
- `README.md`

Placeholders also in the repo: `reports/.gitkeep`, `evidence/screenshots/.gitkeep`, `evidence/traces/.gitkeep`

---

## `.gitignore`

```text
# Python
__pycache__/
*.py[cod]
.pytest_cache/

# Virtual environment
venv/
.venv/

# Playwright default output (this project uses evidence/ instead)
test-results/

# macOS
.DS_Store

# Editors
.idea/
.vscode/
```

---

## `requirements.txt`

```text
pytest>=8.0
pytest-playwright>=0.5
playwright>=1.45
pytest-html>=4.1
```

---

## `pytest.ini`

```ini
[pytest]
testpaths = tests

addopts =
    -v
    --strict-markers
    --tb=short
    --browser chromium
    --screenshot only-on-failure
    --tracing retain-on-failure
    --output evidence
    --html reports/report.html
    --self-contained-html

markers =
    smoke: core checks that must pass before anything else is worth running
    regression: full suite
    login: login and session tests
    products: product list and product detail tests
    cart: cart tests
    checkout: checkout tests
    positive: expected-path behaviour
    negative: invalid input and blocked access
    slow: takes noticeably longer than the rest

log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s %(levelname)s %(message)s
log_cli_date_format = %H:%M:%S
```

---

## `conftest.py`

```python
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
```

---

## `utils/test_data.py`

```python
import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

# Overridable so the suite can point at a different environment.
BASE_URL: str = os.environ.get("SAUCEDEMO_BASE_URL", "https://www.saucedemo.com/")

DATA_FILE: Path = Path(__file__).parent.parent / "test-data" / "users.json"


@lru_cache(maxsize=1)
def load() -> Dict[str, Any]:
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def get_user(key: str) -> Dict[str, str]:
    return load()["users"][key]


def get_all_users() -> Dict[str, Dict[str, str]]:
    return load()["users"]


def get_checkout_info() -> Dict[str, str]:
    return load()["checkout"]


def get_product_name(key: str) -> str:
    return load()["products"][key]


def get_all_products() -> List[str]:
    return list(load()["products"].values())
```

---

## `test-data/users.json`

```json
{
  "users": {
    "valid": {
      "username": "standard_user",
      "password": "secret_sauce"
    },
    "locked_out": {
      "username": "locked_out_user",
      "password": "secret_sauce"
    },
    "problem": {
      "username": "problem_user",
      "password": "secret_sauce"
    },
    "performance_glitch": {
      "username": "performance_glitch_user",
      "password": "secret_sauce"
    },
    "error": {
      "username": "error_user",
      "password": "secret_sauce"
    },
    "visual": {
      "username": "visual_user",
      "password": "secret_sauce"
    },
    "invalid_username": {
      "username": "wrong_user_001",
      "password": "secret_sauce"
    },
    "invalid_password": {
      "username": "standard_user",
      "password": "wrong_pass"
    }
  },
  "checkout": {
    "first_name": "Taro",
    "last_name": "Yamada",
    "postal_code": "220-0011"
  },
  "products": {
    "backpack": "Sauce Labs Backpack",
    "bike_light": "Sauce Labs Bike Light",
    "bolt_tshirt": "Sauce Labs Bolt T-Shirt",
    "fleece_jacket": "Sauce Labs Fleece Jacket",
    "onesie": "Sauce Labs Onesie",
    "red_tshirt": "Test.allTheThings() T-Shirt (Red)"
  }
}
```

---

## `pages/login_page.py`

```python
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
```

---

## `pages/inventory_page.py`

```python
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
```

---

## `pages/product_page.py`

```python
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
```

---

## `pages/cart_page.py`

```python
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
```

---

## `pages/checkout_page.py`

```python
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
```

---

## `tests/test_login.py`

```python
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
```

---

## `tests/test_products.py`

```python
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
```

---

## `tests/test_cart.py`

```python
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
```

---

## `tests/test_checkout.py`

```python
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
```

---

## `docs/test-cases.md`

````markdown
# Test Case Design / テストケース設計

Application: SauceDemo (https://www.saucedemo.com/)
Credentials: standard_user / secret_sauce (published on the login page)

Execution status: not run yet / 未実施

Every test case ID below maps to one test function name in `tests/`.

---

## Login

### TC-LOGIN-001 Valid login redirects to inventory
- Priority: High
- Preconditions: Logged out, on login page
- Test data: standard_user / secret_sauce
- Steps: 1. Enter username. 2. Enter password. 3. Click Login.
- Expected: URL becomes /inventory.html, "Products" header visible, 6 items listed

### TC-LOGIN-002 Invalid username rejected
- Priority: High
- Preconditions: Logged out
- Test data: wrong_user_001 / secret_sauce
- Steps: 1. Enter credentials. 2. Click Login.
- Expected: Error banner containing "do not match any user in this service", no redirect

### TC-LOGIN-003 Invalid password rejected
- Priority: High
- Preconditions: Logged out
- Test data: standard_user / wrong_pass
- Steps: 1. Enter credentials. 2. Click Login.
- Expected: Same error text as TC-LOGIN-002. The application does not reveal which field was wrong.

### TC-LOGIN-004 Required field validation (3 data sets)
- Priority: Medium
- Preconditions: Logged out
- Test data: (a) blank / secret_sauce (b) standard_user / blank (c) blank / blank
- Steps: 1. Fill fields per data set. 2. Click Login.
- Expected: (a) "Username is required" (b) "Password is required" (c) "Username is required"

### TC-LOGIN-005 Locked-out user blocked
- Priority: Medium
- Preconditions: Logged out
- Test data: locked_out_user / secret_sauce
- Steps: 1. Enter credentials. 2. Click Login.
- Expected: Error banner containing "locked out", different from TC-LOGIN-002

### TC-LOGIN-006 Logout returns to login page
- Priority: Medium
- Preconditions: Logged in as standard_user
- Steps: 1. Open burger menu. 2. Click Logout.
- Expected: Login form visible, no longer on /inventory.html

### TC-LOGIN-007 Direct URL access without login is blocked
- Priority: Medium
- Preconditions: Logged out, no session
- Steps: 1. Navigate directly to /inventory.html.
- Expected: Error banner shown and login form visible

---

## Products

### TC-PROD-001 Inventory page lists six products
- Priority: High
- Preconditions: Logged in
- Steps: 1. Observe the product list.
- Expected: Exactly 6 items, all with a non-empty name and a price above zero

### TC-PROD-002 Sorting orders products correctly (4 data sets)
- Priority: Medium
- Preconditions: Logged in
- Test data: Name A-Z, Name Z-A, Price low-high, Price high-low
- Steps: 1. Select sort option. 2. Read displayed order.
- Expected: Displayed order matches the same values sorted in code

### TC-PROD-003 Product detail shows matching data
- Priority: High
- Preconditions: Logged in
- Test data: Sauce Labs Backpack
- Steps: 1. Click the product name. 2. Read the detail page.
- Expected: Name matches the clicked product, description not empty, price starts with $

### TC-PROD-004 Add to cart from inventory updates badge
- Priority: High
- Preconditions: Logged in, empty cart
- Test data: Sauce Labs Backpack
- Steps: 1. Click Add to cart.
- Expected: Badge shows 1, button changes to Remove

### TC-PROD-005 Add to cart from product detail
- Priority: Medium
- Preconditions: Logged in, empty cart
- Test data: Sauce Labs Bike Light
- Steps: 1. Open detail page. 2. Click Add to cart.
- Expected: Badge shows 1, button changes to Remove

### TC-PROD-006 Remove from inventory clears badge
- Priority: Medium
- Preconditions: Logged in, one item in cart
- Steps: 1. Click Remove.
- Expected: Badge not visible at all, button reverts to Add to cart

---

## Cart

### TC-CART-001 Added product appears with correct data
- Priority: High
- Preconditions: Logged in, empty cart
- Test data: Sauce Labs Backpack
- Steps: 1. Record name and price on inventory. 2. Add to cart. 3. Open cart.
- Expected: One row with the recorded name and price

### TC-CART-002 Badge matches number of items
- Priority: Medium
- Preconditions: Logged in, empty cart
- Test data: Backpack, Bike Light
- Steps: 1. Add both. 2. Open cart.
- Expected: Badge shows 2, cart lists both products

### TC-CART-003 Remove from cart empties it
- Priority: High
- Preconditions: Logged in, one item in cart
- Steps: 1. Click Remove on the cart page.
- Expected: Zero rows, badge not visible

### TC-CART-004 Continue shopping returns to inventory
- Priority: Low
- Preconditions: Logged in, on cart page
- Steps: 1. Click Continue Shopping.
- Expected: Back on /inventory.html with the Products header

### TC-CART-005 Cart survives navigation
- Priority: Medium
- Preconditions: Logged in, empty cart
- Steps: 1. Add item. 2. Open cart. 3. Continue shopping. 4. Reopen cart.
- Expected: Item still present, badge still 1

---

## Checkout

### TC-CHK-001 Complete order happy path
- Priority: High
- Preconditions: Logged in, empty cart
- Test data: Backpack. Taro / Yamada / 220-0011
- Steps: 1. Add item. 2. Cart. 3. Checkout. 4. Fill form. 5. Continue. 6. Finish.
- Expected: Reaches /checkout-complete.html, confirmation contains "Thank you for your order", badge cleared

### TC-CHK-002 Required field validation (3 data sets)
- Priority: High
- Preconditions: Logged in, one item in cart, on checkout information page
- Test data: (a) first name blank (b) last name blank (c) postal code blank
- Steps: 1. Fill the other two fields. 2. Click Continue.
- Expected: (a) "First Name is required" (b) "Last Name is required" (c) "Postal Code is required", no navigation

### TC-CHK-003 Overview items and totals
- Priority: High
- Preconditions: Logged in, two items in cart
- Test data: Backpack, Bike Light
- Steps: 1. Checkout with valid information. 2. Read overview.
- Expected: Items match the cart, item total equals the sum of prices, item total plus tax equals total. The tax rate is not hard-coded.

### TC-CHK-004 Cancel returns to cart
- Priority: Low
- Preconditions: Logged in, one item in cart, on checkout information page
- Steps: 1. Click Cancel.
- Expected: Back on /cart.html with the item still in the cart

---

## Summary

| Item | Count |
|---|---|
| Test functions | 22 |
| Executions after parametrization | 29 |
| Positive | 14 |
| Negative / validation | 8 |

## Out of scope

| Excluded | Reason |
|---|---|
| problem_user, error_user, visual_user | Would roughly double the project size for edge cases |
| performance_glitch_user | Timing-based, adds flakiness |
| Visual regression | Needs a baseline image workflow |
| API testing | SauceDemo has no public API |
| Product image assertions | Images are served externally |
````

---

## `README.md`

````markdown
# SauceDemo Playwright + Python UI Automation

UI test automation for SauceDemo, written in Python with Playwright and pytest.

**Status: not run yet / まだ実行していません.** The code is finished but I have not executed the suite. Results and any bugs will go in this README after I run it.

---

# English

## Why I made this

My first QA project was manual testing on EC-CUBE. I wanted to learn automation next, so I needed a site that was simple enough that I could focus on Playwright instead of fighting the application.

SauceDemo works for that. It has a login, six products, a cart and a checkout. Nothing complicated, but enough real steps to practise on.

I kept the project small on purpose. I wanted to be able to explain every file.

## What it tests

24 test functions. With parametrize they run as 31 tests. One is skipped on purpose (problem_user needs image comparison, which I left out of scope).

| Area | Functions | Runs |
|---|---|---|
| Login | 9 | 11 |
| Products | 6 | 9 |
| Cart | 5 | 5 |
| Checkout | 4 | 6 |

Login: valid login, wrong username, wrong password, empty fields, locked out user, logout, opening the inventory URL without logging in.

Products: the product list, all four sort options, the product detail page, adding to the cart from two different screens, removing.

Cart: the item shows up with the right name and price, the count is right with two items, remove, continue shopping, and whether the cart survives moving between pages.

Checkout: the full order flow, the three required fields, the totals on the overview page, and cancelling.

Test case details are in `docs/test-cases.md`.

## Users

Login details are printed on the SauceDemo login page, so nothing here is secret.

| User | Used for |
|---|---|
| standard_user | Normal login and all the main flows |
| locked_out_user | Negative test |

Password: `secret_sauce`

## Setup

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
pytest
```

Other commands I use:

```
pytest --headed              # watch the browser
pytest tests/test_login.py   # one file
pytest -k login              # match by keyword
```

Chromium is the default. Firefox and WebKit work too:

```
pytest --browser chromium --browser firefox --browser webkit
```

I did not make three browsers the default. SauceDemo behaves the same in all of them, so I would be running three times as many tests for the same result.

## How I structured it

Page Object Model. Locators live in `pages/`, the checks live in `tests/`.

| File | What it covers |
|---|---|
| `pages/login_page.py` | Login form, error banner |
| `pages/inventory_page.py` | Product list, sorting, cart badge, menu |
| `pages/product_page.py` | Product detail page |
| `pages/cart_page.py` | Cart contents and buttons |
| `pages/checkout_page.py` | All three checkout steps |

I put the assertions in the tests, not in the page objects. If I hid them inside the page object I would have to open two files to see what a test actually checks.

`conftest.py` has two fixtures. One opens the login page. The other logs in and hands back the inventory page, so the product, cart and checkout tests do not repeat login steps.

## Locators

Mostly `[data-test="..."]`, because SauceDemo puts those attributes on elements specifically for testing. They do not move when the design changes.

For buttons I used `get_by_role("button", name="Add to cart")`. It reads like what a person sees on screen.

For the sort dropdown I used `get_by_role("combobox")` since there is only one select on the page.

For product cards I used `.filter(has_text="Sauce Labs Backpack")` to narrow down to one card first. Without that, clicking "Add to cart" would hit whichever button Playwright found first, which is not necessarily the product I wanted.

## Things I want to check when I run it

Three things I am not sure about, and I will update this section with what actually happens:

1. TC-LOGIN-007. I expect an error when you open `/inventory.html` without logging in, but I have not confirmed the exact behaviour.
2. The cart page might use a different `data-test` value than the inventory page for its item rows.
3. The exact wording of the error messages. I used partial matching so small differences do not break the tests, but I still need to see the real text.

## What I learned building it

The cart badge confused me. When the cart is empty the badge element is not there at all, it does not show "0". So `cart_count()` returns 0 when the element is missing instead of trying to read text from something that does not exist. I would have written that wrong if I had assumed it worked like a normal counter.

Playwright waits by itself. `expect(...).to_have_text("1")` retries until the text appears or it times out. Coming from tutorials full of `time.sleep()`, this took a while to trust. There is no `sleep` anywhere in this project.

Hard-coding expected values is fragile. In the cart test I read the price from the product list first, then check the cart shows the same price. If Sauce Labs changes a price tomorrow, the test still passes, because it is checking that the data carries over correctly, not that the backpack costs $29.99.

Same idea in the checkout test. I do not hard-code the tax rate. I check that item total plus tax equals the final total.

## Limitations

SauceDemo has no backend. There is no order number and no order history, so checkout verification stops at the confirmation message on screen.

The cart is stored in the browser, so tests need a clean browser context each time. pytest-playwright does this by default. Without it, one test's cart would leak into the next test.

Sauce Labs can change the site, and then the locators need updating.

Test data is fixed. Same product, same form values every run.

## Results

Not run yet / 未実施

## Bugs

None recorded yet. Anything I find will go in `docs/bugs.md`.

## Environment

| Item | Value |
|---|---|
| OS | macOS |
| Python | Not recorded yet |
| Playwright | Not recorded yet |
| pytest | Not recorded yet |
| Browser | Chromium |
| Run date | Not run yet |

## Structure

```
02-saucedemo-playwright-python/
├── README.md
├── requirements.txt
├── pytest.ini
├── .gitignore
├── conftest.py
├── tests/
│   ├── test_login.py
│   ├── test_products.py
│   ├── test_cart.py
│   └── test_checkout.py
├── pages/
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── utils/
│   └── test_data.py
├── test-data/
│   └── users.json
├── docs/
│   └── test-cases.md
├── reports/
└── evidence/
    ├── screenshots/
    └── traces/
```

## Next

- Run the suite and record the real results here
- Add GitHub Actions so it runs automatically
- Try `problem_user`, which is a version of the site with deliberate bugs
- Move the base URL out into an environment variable

## Author

Tmg

---

# 日本語

## 作った理由

最初のQAプロジェクトは EC-CUBE の手動テストでした。次は自動化を覚えたかったので、アプリ自体で苦労せずに Playwright に集中できる、シンプルなサイトを探していました。

SauceDemo はその条件に合っています。ログイン、商品6件、カート、チェックアウトがあります。複雑ではありませんが、練習するには十分な流れがあります。

規模はあえて小さくしました。全部のファイルを自分で説明できる状態にしたかったからです。

## テストしている内容

テスト関数は24件、parametrize を含めると31件です。1件は意図的にスキップしています(problem_user は画像比較が必要で、今回は対象外にしました)。

| 領域 | 関数 | 実行数 |
|---|---|---|
| ログイン | 9 | 11 |
| 商品 | 6 | 9 |
| カート | 5 | 5 |
| チェックアウト | 4 | 6 |

ログイン: 正常ログイン、ユーザー名の誤り、パスワードの誤り、未入力、ロックされたユーザー、ログアウト、未ログイン状態での商品一覧URLへの直接アクセス。

商品: 商品一覧、並び替え4種類、商品詳細ページ、2つの画面からのカート追加、削除。

カート: 商品名と価格が正しく表示されるか、2件入れたときの件数、削除、買い物を続ける、画面を移動してもカートが残るか。

チェックアウト: 注文完了までの流れ、必須3項目、確認画面の金額、キャンセル。

テストケースの詳細は `docs/test-cases.md` にあります。

## 使用ユーザー

ログイン情報は SauceDemo のログイン画面に表示されているものなので、秘密の情報ではありません。

| ユーザー | 用途 |
|---|---|
| standard_user | 通常ログインと主要な流れ |
| locked_out_user | 異常系 |

パスワード: `secret_sauce`

## 実行方法

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
pytest
```

よく使うコマンド:

```
pytest --headed              # ブラウザを表示して実行
pytest tests/test_login.py   # ファイル単位
pytest -k login              # キーワードで絞る
```

既定は Chromium です。Firefox と WebKit でも動きます。

```
pytest --browser chromium --browser firefox --browser webkit
```

3ブラウザを既定にはしませんでした。SauceDemo はどのブラウザでも同じ動きなので、実行数だけ3倍になって結果は変わらないと考えたからです。

## 構成の考え方

Page Object Model を使っています。ロケーターは `pages/` に、確認内容は `tests/` に置いています。

| ファイル | 対象 |
|---|---|
| `pages/login_page.py` | ログインフォーム、エラー表示 |
| `pages/inventory_page.py` | 商品一覧、並び替え、カートバッジ、メニュー |
| `pages/product_page.py` | 商品詳細ページ |
| `pages/cart_page.py` | カートの内容とボタン |
| `pages/checkout_page.py` | チェックアウト3ステップ |

アサーションはページオブジェクトではなくテスト側に書いています。ページオブジェクトの中に隠すと、そのテストが何を確認しているのか見るのに2つのファイルを開くことになるためです。

`conftest.py` には fixture が2つあります。1つはログイン画面を開くもの、もう1つはログインして商品一覧を返すものです。商品、カート、チェックアウトのテストでログイン手順を繰り返さずに済みます。

## ロケーターについて

基本は `[data-test="..."]` です。SauceDemo はテスト用にこの属性を付けてくれているので、デザインが変わっても影響を受けにくいです。

ボタンは `get_by_role("button", name="Add to cart")` を使いました。画面上の表示そのままなので読みやすいです。

並び替えのプルダウンは `get_by_role("combobox")` です。ページ内に select が1つしかないためです。

商品カードは `.filter(has_text="Sauce Labs Backpack")` で先に1件に絞っています。これをしないと「Add to cart」ボタンが複数あるので、意図しない商品を押してしまいます。

## 実行時に確認したいこと

自信がない箇所が3つあります。実行後にここを更新します。

1. TC-LOGIN-007。未ログインで `/inventory.html` を開くとエラーになるはずですが、実際の挙動は未確認です。
2. カート画面の行が、商品一覧と同じ `data-test` の値かどうか。
3. エラーメッセージの正確な文言。部分一致で書いているので多少の差なら壊れませんが、実際の文言は確認が必要です。

## 作っていて分かったこと

カートバッジで一度つまずきました。カートが空のときはバッジが「0」と表示されるのではなく、要素自体が存在しません。なので `cart_count()` は要素がない場合に 0 を返すようにしています。普通のカウンターだと思い込んでいたら間違ったコードを書いていました。

Playwright は自動で待ってくれます。`expect(...).to_have_text("1")` はテキストが出るまで再試行します。`time.sleep()` だらけのチュートリアルを見ていたので、最初は信用しきれませんでした。このプロジェクトに sleep は1つもありません。

期待値の直書きは壊れやすいと感じました。カートのテストでは先に商品一覧から価格を取得し、カートに同じ価格が出ているかを確認しています。価格が変わってもテストは通ります。確認したいのは「バックパックが29.99ドルであること」ではなく「データが正しく引き継がれること」だからです。

チェックアウトも同じ考え方で、税率は直書きしていません。商品合計と税を足したものが合計と一致するかを見ています。

## 制約

SauceDemo にはバックエンドがありません。注文番号も注文履歴もないので、チェックアウトの確認は画面上の完了メッセージまでです。

カートはブラウザ側に保存されるため、テストごとに新しいブラウザコンテキストが必要です。pytest-playwright が既定でやってくれます。これがないと前のテストのカートが次に残ります。

Sauce Labs 側でサイトが変わればロケーターの修正が必要になります。

テストデータは固定です。毎回同じ商品、同じ入力値を使っています。

## 結果

未実施

## 不具合

まだ記録はありません。見つかったものは `docs/bugs.md` に書きます。

## 環境

| 項目 | 内容 |
|---|---|
| OS | macOS |
| Python | 未記録 |
| Playwright | 未記録 |
| pytest | 未記録 |
| ブラウザ | Chromium |
| 実行日 | 未実施 |

## 今後

- 実行して結果をここに記載する
- GitHub Actions で自動実行できるようにする
- 意図的に不具合が入っている `problem_user` を試す
- ベースURLを環境変数に切り出す

## 作成者

Tmg

---

## Markers

```
pytest -m smoke       # 7 core tests
pytest -m negative    # invalid input and blocked access
pytest -m login       # one area
pytest -m "not slow"  # skip the performance_glitch_user test
```
````

---

