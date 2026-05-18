## メダリオンアーキテクチャとは
- データを「段階的に品質あげながら保存する」設計パターン
- DataBricksが提唱し、データレイクハウスの標準的な構成となっている

### 3層の役割

#### Bronze 「まず全て受け取る」
- 生データをそのまま保存。変換・クレンジングは行わない
- 目的として元データを失わない、何かあれば再処理できる

#### Silver 「使える状態にする」
- 型変換・NULL除去・重複排除・フォーマット統一
- 目的としてどのチームが使っても安全なクリーンなデータにする

#### Gold 「答えを出す」
- ビジネスロジックを適用した集計・加工済みテーブル
- 目的としてBIツールやレポートにそのまま使える形にする

### なぜ層を分けるのか
- 層を分けずに生データから直接集計すると
  - 汚れデータが混入した計算結果に気づけない
  - 再処理する時「どこまで戻ればいいか」がわからない
  - チームによって異なるクレンジングロジックが乱立する
- **層ごとに責務を分けることで、問題が起きたときにどの層に原因があるかが即座にわかるのが最大のメリット**

#### 実務での位置付け
| ツール                         | 役割                    |
  |-----------------------------|-----------------------|
  | Delta Lake / Apache Iceberg | ストレージフォーマット（層ごとに管理）   |
  | Databricks / Apache Spark   | 大規模データの処理エンジン         |
  | dbt                         | Silver/Gold層の変換ロジック管理 |
  | Apache Airflow              | パイプラインのスケジューリング       |

このプロジェクト         実務規模
  ─────────────────────────────────────
  CSV（生データ）      →  S3 / ADLS
  pandas               →  Spark / Polars
  手動実行             →  Airflow / Dagster
  ファイル保存         →  Delta Lake / Parquet

## ClaudeCodeに作成させたプロジェクト

### 構成
```sh
.
├── data
│   ├── bronze
│   │   └── orders.csv
│   ├── gold
│   │   ├── customer_summary.csv
│   │   ├── monthly_sales.csv
│   │   └── product_ranking.csv
│   ├── raw
│   │   └── orders.csv
│   └── silver
│       └── orders.csv
├── docs
│   └── scripts.md
├── main.py
└── pyproject.toml
```

### `main.py`

```python
```

## `main.py`よりメダリオンアーキテクチャを理解する

### Step0 `generate_raw()`生データ生成
100件の注文データを生成します。実務で起こりうる以下の「汚れ」を意図的に混入させている。

| 汚れの種類 | 内容 | 発生確率 |
|---|---|---|
| 欠損値 | `quantity` または `unit_price` が空欄 | 各5% |
| 日付フォーマット混在 | `YYYY-MM-DD` と `DD/MM/YYYY` が混在 | 20% |
| 重複レコード | 同じ `order_id` を持つ注文が複数存在 | 5% |

#### 日付フォーマット混在
```python
# 日付フォーマットを 20% の確率で DD/MM/YYYY に変える（汚れ①）
delta       = end - start
dt          = start + timedelta(days=random.randint(0, delta.days))
order_date  = dt.strftime("%d/%m/%Y") if random.random() < 0.2 else dt.strftime("%Y-%m-%d")
```

#### 欠損値
```python
"quantity":    quantity if random.random() > 0.05 else "",   # 汚れ②: 5% で空欄
```

#### 重複レコード
```python
 if random.random() < 0.05:
            row["order_id"] = f"ORD-{random.randint(1, i):04d}"
```

### Step1 `load_to_bronze()`Bronze層
生データを**そそまま**取り込む。変換クレンジングは一切行わない。
ンマデータを保存しておくことで後から再処理が楽になる

<主な処理>
- 全カラムを文字列として読み込む
- 読み込み日時とファイル名を付与して保存


### Step2　 `standardize_date()/transform_to_silver()`Silever層
Bronze層のデータをクレンジング・標準化します
`standardize_date()`で日時形式を統一

<主な処理>
- `quantity`,`price`を数値型に変換(できないものは除外)
- `order_date`のフォーマットを統一(できないものは除外)
- `order_id`が重複している場合は一見だけ残す
- 合計金額計算

### Step3 `build_gold()` Gold層
Silver データから3種類の集計テーブルを作成して保存する

<主な処理>
- 月別売上サマリー（注文数・売上合計）
- 商品別売上ランキング（売上金額順）
- 顧客別購入サマリー（購入回数・合計金額・平均単価）


## メダリオンアーキテクチャを学んで
























