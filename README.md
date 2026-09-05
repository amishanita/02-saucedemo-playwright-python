# SauceDemo Playwright + Python UI Automation

UI test automation for SauceDemo, written in Python with Playwright and pytest.

**Status: run on 2026-09-03. 30 passed, 1 skipped (Chromium).** Details in the Results section below.

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

## Things I was unsure about, and how they turned out

I had three question marks before the first real run:

1. TC-LOGIN-007. Opening `/inventory.html` without logging in. It does get blocked with an error, so the test passed.
2. Whether the cart page uses the same item locator as the inventory page. It does.
3. The exact error message wording. Partial matching held up, so I did not have to change anything.

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

Run on 2026-09-03, Chromium, on macOS.

| Result | Count |
|---|---|
| Passed | 30 |
| Skipped | 1 |
| Failed | 0 |
| Total | 31 |

Run time was about 32 seconds.

The one skipped test is `test_login_008_problem_user_visual_issues`. I skipped it on purpose. `problem_user` shows broken product images, and checking images properly needs visual comparison, which I decided was out of scope for this project. The skip reason is written in the test so it shows up in the report instead of being silently ignored.

Everything else passed on the first real run. Two things I had been unsure about turned out fine: opening `/inventory.html` without logging in does get blocked (TC-LOGIN-007), and the cart page uses the same `data-test` item locator as the inventory page.

The HTML report is at `reports/report.html` after a run.

## Bugs

No defects were found in the automated scope. I tested with `standard_user`, which is the clean account, so this is the expected result. See `docs/bugs.md` for the short write-up.

I did not test the deliberately broken accounts (`problem_user`, `error_user`) beyond the one skipped test. Those would be a separate piece of work.

## Environment

| Item | Value |
|---|---|
| OS | macOS |
| Python | 3.14.7 |
| Playwright | 1.62.0 |
| pytest | 9.1.1 |
| Browser | Chromium |
| Run date | 2026-09-03 |

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

- Add GitHub Actions so it runs automatically
- Try `problem_user`, which is a version of the site with deliberate bugs
- Move the base URL out into an environment variable

## Author

Tamang Amish

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

## 実行前に不安だった点と、その結果

最初の実行前に自信がない箇所が3つありました。

1. TC-LOGIN-007。未ログインで `/inventory.html` を開いたとき。ブロックされてエラーが出たので、テストは成功しました。
2. カート画面が商品一覧と同じロケーターかどうか。同じでした。
3. エラーメッセージの正確な文言。部分一致で書いていたので、修正は不要でした。

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

2026年9月3日に Chromium で実行しました。

| 結果 | 件数 |
|---|---|
| 成功 | 30 |
| スキップ | 1 |
| 失敗 | 0 |
| 合計 | 31 |

実行時間は約32秒でした。

スキップした1件は `test_login_008_problem_user_visual_issues` です。これは意図的にスキップしています。`problem_user` は商品画像が壊れており、画像を正しく確認するには画像比較が必要で、今回は対象外にしたためです。スキップの理由はテスト内に書いてあるので、レポートにも表示されます。

それ以外は最初の実行で全て成功しました。不安だった2点も問題ありませんでした。未ログインで `/inventory.html` を開くとブロックされること(TC-LOGIN-007)、カート画面が商品一覧と同じ `data-test` を使っていることです。

実行後、HTMLレポートは `reports/report.html` に出力されます。

## 不具合

自動化の対象範囲では不具合は見つかりませんでした。`standard_user` はクリーンなアカウントなので、この結果は想定通りです。詳細は `docs/bugs.md` に書いています。

意図的に壊されているアカウント(`problem_user`、`error_user`)は、スキップした1件以外はテストしていません。これは別の作業として扱うべき内容です。

## 環境

| 項目 | 内容 |
|---|---|
| OS | macOS |
| Python | 3.14.7 |
| Playwright | 1.62.0 |
| pytest | 9.1.1 |
| ブラウザ | Chromium |
| 実行日 | 2026-09-03 |

## 今後

- GitHub Actions で自動実行できるようにする
- 意図的に不具合が入っている `problem_user` を試す
- ベースURLを環境変数に切り出す

## 作成者

Tamang Amish

---

## Markers

```
pytest -m smoke       # 7 core tests
pytest -m negative    # invalid input and blocked access
pytest -m login       # one area
pytest -m "not slow"  # skip the performance_glitch_user test
```
