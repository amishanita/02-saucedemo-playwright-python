# 02 / SauceDemo UI自動テスト（Python + Playwright + pytest）

ECサイトのデモアプリ [SauceDemo](https://www.saucedemo.com/) を対象に、Page Object Model で組んだUI自動テストです。[01](https://github.com/amishanita/01-eccube-manual-qa) で手で設計したテストのうち、毎回同じことを繰り返す部分を自動化しました。

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Playwright](https://img.shields.io/badge/Playwright-2EAD33?logo=playwright&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?logo=pytest&logoColor=white)

## 結果

| 項目 | 数 |
|---|---:|
| テスト関数 | 24 |
| 実行ケース（パラメータ展開後） | 31 |
| 成功 | 30 |
| スキップ | 1 |
| 失敗 | 0 |

実行日：2026年9月3日
スキップの1件は対象アプリ側の既知の挙動に対する意図的なものです。理由はテストコードに書いてあります。

## 設計で決めたこと

### 画面の定義とテストの手順を分ける

セレクタは Page クラスにまとめて、テスト関数には何を確認するかだけを書いています。

```
pages/     画面ごとのクラス。セレクタと操作を持つ
tests/     何を確認するか。セレクタは書かない
```

自動テストが壊れる原因で一番多いのがセレクタの変更です。UIが変わったときに直す場所が1か所で済むようにしておかないと、いずれ保守できなくなります。

### pytest のマーカーで実行範囲を切り替える

| マーカー | 用途 |
|---|---|
| `smoke` | これが通らないとリリースできない導線 |
| `regression` | 変更の影響を確認する一式 |
| `negative` | 異常系（不正なログイン、空のカートなど） |

```bash
pytest -m smoke        # 主要導線だけ、短時間
pytest -m regression   # 全体
```

毎回全部流すと時間がかかるので、用途で分けられるようにしました。この分け方をそのまま [04](https://github.com/amishanita/04-saucedemo-ci-cd-qa) のCIに持っていっています。

### fixture で前提条件をまとめる

ブラウザの起動と終了、ログイン済みの状態は fixture に寄せて、各テストには確認したいことだけが残るようにしました。

### 型ヒントをつける

Page クラスとヘルパー関数に型ヒントを書いています。テストコードも後から人が読むので、本番コードと同じ基準で書いたほうがいいと思っています。

## テストした範囲

| 分類 | 内容 |
|---|---|
| ログイン | 正常ログイン、ロックされたユーザー、不正な認証情報、空欄 |
| 商品一覧 | 表示件数、価格と名前のソート |
| カート | 追加、削除、件数バッジ、カート内表示 |
| チェックアウト | 情報入力、入力漏れ時のエラー、合計金額の計算、注文完了 |
| ログアウト | セッションの破棄 |

カートからチェックアウト、注文完了までの流れを最優先にしています。

## 実行方法

```bash
pip install -r requirements.txt
playwright install chromium

pytest                          # 全部
pytest -m smoke                 # 主要導線だけ
pytest --html=report.html --self-contained-html
pytest --headed --slowmo 500    # ブラウザを見ながら実行
```

## リポジトリ構成

```
.
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   └── test_checkout.py
├── conftest.py          fixture
├── pytest.ini           マーカー定義
├── requirements.txt
└── README.md
```

【要確認：実際のファイル名に合わせて書き換える】

## 環境

Python 3.12、Playwright（Chromium）、pytest、macOS 15.7（Intel MacBook Pro）

## やってみて分かったこと

自動テストは、書く時間より後から直す時間のほうが長くなります。セレクタをテストコードに直接書かないようにしただけで、UIが変わったときの修正量がかなり変わりました。

全部自動化するのは目的になりません。実行が安定しないものや、結果の判断に人の目が要るものは手動で残したほうが結果的に速いです。何を自動化して何を残すかを決めるほうに時間を使いました。

落ちたテストを見たときに、アプリの不具合なのかテストコードの不備なのかがすぐ分からないと、そのうち誰も結果を見なくなります。失敗時にスクリーンショットとログが残るようにしてあります。

## 次にやること

- GitHub Actions で自動実行（[04](https://github.com/amishanita/04-saucedemo-ci-cd-qa)）
- JSTQB Foundation Level 受験（2026年11月11日）

## 関連リポジトリ

| | 内容 |
|---|---|
| [01](https://github.com/amishanita/01-eccube-manual-qa) | EC-CUBE 手動テスト設計・不具合報告 |
| 02（このリポジトリ） | Playwright と pytest によるUI自動テスト |
| [03](https://github.com/amishanita/03-restful-booker-api-automation) | REST API のテストと不具合検出 |
| [04](https://github.com/amishanita/04-saucedemo-ci-cd-qa) | GitHub Actions による自動実行 |

---

# English

# 02 / SauceDemo UI Automation (Python + Playwright + pytest)

UI automation for [SauceDemo](https://www.saucedemo.com/), built on the Page Object Model. It covers the parts of the manual suite from [01](https://github.com/amishanita/01-eccube-manual-qa) that get repeated every time.

## Results

| Item | Count |
|---|---:|
| Test functions | 24 |
| Executed cases | 31 |
| Passed | 30 |
| Skipped | 1 |
| Failed | 0 |

Run on 3 September 2026. The skip is deliberate, against a known behaviour of the application, and the reason is in the test.

## Design decisions

**Selectors live in page classes, not in tests.** Tests say what is being checked; the page classes know how to find things. Selector changes are the most common reason a UI suite rots, so there's one place to fix when the interface moves.

**pytest markers** (`smoke`, `regression`, `negative`) so the suite can run at different sizes. Running everything every time takes too long, and the same split carries into the CI setup in [04](https://github.com/amishanita/04-saucedemo-ci-cd-qa).

**Fixtures** handle browser lifecycle and logged-in state, so each test contains only its own assertion.

**Type hints** on page classes and helpers. Test code gets read by people too.

## Coverage

Login (valid, locked-out user, bad credentials, empty fields), product listing and sorting, cart add/remove/badge, checkout including validation and totals, logout. Cart to checkout to order complete is the priority.

## Running it

```bash
pip install -r requirements.txt
playwright install chromium
pytest
pytest -m smoke
pytest --headed --slowmo 500
```

## Environment

Python 3.12, Playwright (Chromium), pytest, macOS 15.7.

## What I learned

Maintaining a suite takes longer than writing one. Keeping selectors out of the tests made a noticeable difference the first time the UI changed.

Automating everything isn't the goal. Some checks are faster and more reliable done by hand, and deciding which ones took more thought than the code did.

If you can't tell quickly whether a red test means a broken app or a broken test, people stop reading the results. Failures save a screenshot and the log.

## Next

CI with GitHub Actions ([04](https://github.com/amishanita/04-saucedemo-ci-cd-qa)). JSTQB Foundation Level on 11 November 2026.

**Tamang Amish** — [GitHub](https://github.com/amishanita) / [LinkedIn](https://www.linkedin.com/in/tamang-amish-669289250)
