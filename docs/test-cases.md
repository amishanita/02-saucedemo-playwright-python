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
