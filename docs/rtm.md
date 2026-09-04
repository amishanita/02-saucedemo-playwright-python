# Requirements Traceability Matrix (RTM) / 要件トレーサビリティマトリクス

Project: SauceDemo Playwright + Python UI Automation
Run date / 実行日: 2026-09-03
Environment: macOS, Chromium, Python 3.14.7, Playwright 1.62.0, pytest 9.1.1

---

## About this document / この文書について

SauceDemo has no formal requirements document, so the requirements below are derived from the application's observable behavior. Each requirement maps to at least one test case, each test case maps to a real test function in the code, and each row shows the actual run status.

SauceDemo には正式な要件定義書がないため、以下の要件はアプリケーションの動作から導き出しています。各要件は少なくとも1つのテストケースに対応し、各テストケースはコード内の実際のテスト関数に対応します。ステータスは実行結果を反映しています。

---

## Summary / サマリ

| Item / 項目 | Count / 件数 |
|---|---|
| Requirements / 要件 | 20 |
| Test cases / テストケース | 22 |
| Test functions / テスト関数 | 24 |
| Test executions / 実行数 | 31 |
| Passed / 成功 | 30 |
| Skipped / スキップ | 1 |
| Failed / 失敗 | 0 |
| Requirements coverage / 要件カバレッジ | 100% |

---

## Login / ログイン

| Req ID | Requirement | Test Case ID | Test Function | Status |
|---|---|---|---|---|
| REQ-LOGIN-01 | Valid user can log in and reach the inventory page | TC-LOGIN-001 | test_login_001_valid_login_redirects_to_inventory | ✅ PASS |
| REQ-LOGIN-02 | System rejects unknown username | TC-LOGIN-002 | test_login_002_invalid_username_is_rejected | ✅ PASS |
| REQ-LOGIN-03 | System rejects wrong password | TC-LOGIN-003 | test_login_003_invalid_password_is_rejected | ✅ PASS |
| REQ-LOGIN-04 | System validates required fields (username, password) | TC-LOGIN-004 | test_login_004_required_field_validation (3 runs) | ✅ PASS |
| REQ-LOGIN-05 | System blocks locked-out user with distinct message | TC-LOGIN-005 | test_login_005_locked_out_user_is_blocked | ✅ PASS |
| REQ-LOGIN-06 | Logged-in user can log out | TC-LOGIN-006 | test_login_006_logout_returns_to_login_page | ✅ PASS |
| REQ-LOGIN-07 | Direct URL access without session is blocked | TC-LOGIN-007 | test_login_007_direct_url_access_without_login_is_blocked | ✅ PASS |
| REQ-LOGIN-08 | Slow user (performance_glitch) can still complete login | TC-LOGIN-009 | test_login_009_performance_glitch_user_can_still_log_in | ✅ PASS |

Note: TC-LOGIN-008 (problem_user visual issues) is skipped on purpose because it requires visual comparison, which is out of scope.

---

## Products / 商品

| Req ID | Requirement | Test Case ID | Test Function | Status |
|---|---|---|---|---|
| REQ-PROD-01 | Inventory displays 6 products with name and price | TC-PROD-001 | test_prod_001_inventory_page_lists_six_products | ✅ PASS |
| REQ-PROD-02 | User can sort products (name A-Z, Z-A, price low-high, high-low) | TC-PROD-002 | test_prod_002_sorting_orders_products_correctly (4 runs) | ✅ PASS |
| REQ-PROD-03 | Product detail page shows correct name, description, price | TC-PROD-003 | test_prod_003_product_detail_shows_matching_data | ✅ PASS |
| REQ-PROD-04 | User can add product to cart from inventory page | TC-PROD-004 | test_prod_004_add_to_cart_from_inventory_updates_badge | ✅ PASS |
| REQ-PROD-05 | User can add product to cart from product detail page | TC-PROD-005 | test_prod_005_add_to_cart_from_product_detail | ✅ PASS |
| REQ-PROD-06 | User can remove product from cart via inventory page | TC-PROD-006 | test_prod_006_remove_from_inventory_clears_badge | ✅ PASS |

---

## Cart / カート

| Req ID | Requirement | Test Case ID | Test Function | Status |
|---|---|---|---|---|
| REQ-CART-01 | Cart shows added product with correct name and price | TC-CART-001 | test_cart_001_added_product_appears_with_correct_data | ✅ PASS |
| REQ-CART-02 | Cart badge count matches number of items | TC-CART-002 | test_cart_002_badge_matches_number_of_items | ✅ PASS |
| REQ-CART-03 | User can remove product from cart page | TC-CART-003 | test_cart_003_remove_from_cart_empties_it | ✅ PASS |
| REQ-CART-04 | User can return to inventory via "Continue Shopping" | TC-CART-004 | test_cart_004_continue_shopping_returns_to_inventory | ✅ PASS |
| REQ-CART-05 | Cart contents persist across page navigation | TC-CART-005 | test_cart_005_cart_survives_navigation | ✅ PASS |

---

## Checkout / チェックアウト

| Req ID | Requirement | Test Case ID | Test Function | Status |
|---|---|---|---|---|
| REQ-CHK-01 | User can complete full checkout flow to order confirmation | TC-CHK-001 | test_chk_001_complete_order_happy_path | ✅ PASS |
| REQ-CHK-02 | Checkout form validates required fields (first name, last name, postal code) | TC-CHK-002 | test_chk_002_required_field_validation (3 runs) | ✅ PASS |
| REQ-CHK-03 | Overview page shows correct items and totals (item total + tax = total) | TC-CHK-003 | test_chk_003_overview_items_and_totals | ✅ PASS |
| REQ-CHK-04 | User can cancel checkout and return to cart | TC-CHK-004 | test_chk_004_cancel_returns_to_cart | ✅ PASS |

---

## Coverage analysis / カバレッジ分析

**By area / 領域別:**

| Area / 領域 | Requirements | Test Cases | Coverage |
|---|---|---|---|
| Login / ログイン | 8 | 8 | 100% |
| Products / 商品 | 6 | 6 | 100% |
| Cart / カート | 5 | 5 | 100% |
| Checkout / チェックアウト | 4 | 4 | 100% |
| **Total** | **23** | **23** | **100%** |

**By test type / テスト種別:**

| Type / 種別 | Count / 件数 |
|---|---|
| Positive / 正常系 | 14 |
| Negative / 異常系 | 8 |
| Total functions / 合計関数 | 24 (including 1 skipped / 1件スキップ含む) |

---

## Out of scope / 対象外

The following areas have no requirements traced because they were deliberately excluded from the project scope. These are documented in the README under "Limitations."

以下の領域はプロジェクトのスコープから意図的に除外したため、要件を紐づけていません。詳細は README の「制約」に記載しています。

| Excluded / 対象外 | Reason / 理由 |
|---|---|
| Visual regression / ビジュアルリグレッション | Requires baseline image workflow / 基準画像の運用が必要 |
| problem_user, error_user, visual_user | Deliberately broken accounts; would double project scope / 意図的に壊されたアカウント、規模が倍になる |
| API testing / API テスト | SauceDemo has no public API / SauceDemo に公開 API がない |
| Product image assertions / 商品画像の検証 | Images served externally / 画像が外部から配信されている |
| Cross-browser as default / 既定でのクロスブラウザ | Chromium only by default; other browsers available via command flag / 既定は Chromium のみ、他ブラウザはコマンドで利用可能 |
