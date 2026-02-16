# 自然言語からMCPでmermaidにてフローチャート作成

## 利用しているnodeのバージョン
```
v24.10.0
```

## そもそもMCPとは
- AIがほかツールを安全に呼び出すための共通規格

## mcp インストール
```bash
$ npm install -g mermaid-mcp-server
```

## Cline（VSCode拡張)の準備

<img width="1024" height="806" alt="スクリーンショット 2026-02-14 21 39 56" src="https://github.com/user-attachments/assets/f65360e6-fbf1-456f-ace8-7c419d8766ca" />

## cline_mcp_setting.json

<img width="1470" height="956" alt="スクリーンショット 2026-02-14 21 14 29" src="https://github.com/user-attachments/assets/fe10ec34-aaed-4419-80c0-b65da87271b5" />

```json
{
  "mcpServers": {
    "mermaid-mcp-server": {
      "command": "mermaid-mcp-server",
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

## とりあえず使ってみる
プロンプト
```
以下の文章を Mermaid の flowchart で表現して

・「分岐は菱形、開始/終了は丸、例外は点線」
・「日本語ラベルは必ずダブルクォートで囲む」
・「生成後に validate_mermaid を実行し、通らなければ修正して」
・「最後に render_mermaid_svg でSVG化して」

下記内容で作成して
ユーザーが申請 → 入力チェック → OKなら承認依頼 → 承認なら完了、否認なら差し戻し → 入力チェックへ戻る
```

## やってみた結果
```mermaid
flowchart TD
    A["ユーザーが申請"] --> B{"入力チェック"}
    B -->|"OK"| C["承認依頼"]
    B -->|"NG"| D["差し戻し"]
    C -->|"承認"| E["完了"]
    C -->|"否認"| D
    D -.->|"再入力"| B
```

<img width="1470" height="828" alt="スクリーンショット 2026-02-14 21 33 19" src="https://github.com/user-attachments/assets/de3cf37c-b582-4c5b-83a9-b1982f3e07a0" />


## ER図

プロンプト
```
以下の業務説明から Mermaid の erDiagram を生成してください。

【要件】
- 必ず erDiagram 構文を使用する
- すべてのエンティティに主キーを定義する
- 外部キーを明示する
- データ型を必ず記載する（int, string, datetime, boolean など）
- リレーションには多重度を必ず明示する（||--o{ など）
- 中間テーブルが必要な場合は作成する
- エンティティ名は英語の単数形にする
- 属性名も英語にする
- 日本語説明はコメントとして残す
- コードブロックは mermaid 形式で出力する
- 構文エラーがないか自己チェックする

【業務説明】

・ユーザーは会員登録を行う  
・ユーザーは複数の注文を持つ  
・注文には複数の商品が含まれる  
・商品は複数の注文に含まれる  
・商品には在庫数がある  
・注文には支払いステータス（未払い、支払済み、キャンセル）がある  
・ユーザーは複数の配送先住所を登録できる  
・注文は1つの配送先住所を指定する
```

生成結果

```mermaid
erDiagram
    %% ユーザー - 会員登録を行う
    User {
        int userId PK "ユーザーID"
        string username "ユーザー名"
        string email "メールアドレス"
        string passwordHash "パスワードハッシュ"
        datetime createdAt "作成日時"
        datetime updatedAt "更新日時"
    }

    %% 配送先住所 - ユーザーは複数の配送先住所を登録できる
    ShippingAddress {
        int addressId PK "住所ID"
        int userId FK "ユーザーID"
        string recipientName "受取人名"
        string postalCode "郵便番号"
        string prefecture "都道府県"
        string city "市区町村"
        string addressLine1 "住所1"
        string addressLine2 "住所2"
        string phoneNumber "電話番号"
        boolean isDefault "デフォルト住所フラグ"
        datetime createdAt "作成日時"
    }

    %% 注文 - ユーザーは複数の注文を持つ、注文は1つの配送先住所を指定する
    Order {
        int orderId PK "注文ID"
        int userId FK "ユーザーID"
        int shippingAddressId FK "配送先住所ID"
        string orderStatus "注文ステータス"
        string paymentStatus "支払いステータス"
        decimal totalAmount "合計金額"
        datetime orderDate "注文日時"
        datetime updatedAt "更新日時"
    }

    %% 商品 - 商品は複数の注文に含まれる、商品には在庫数がある
    Product {
        int productId PK "商品ID"
        string productName "商品名"
        string description "商品説明"
        decimal price "価格"
        int stockQuantity "在庫数"
        string category "カテゴリ"
        boolean isActive "有効フラグ"
        datetime createdAt "作成日時"
        datetime updatedAt "更新日時"
    }

    %% 注文明細 - 中間テーブル（注文と商品の多対多関係）
    OrderItem {
        int orderItemId PK "注文明細ID"
        int orderId FK "注文ID"
        int productId FK "商品ID"
        int quantity "数量"
        decimal unitPrice "単価"
    }

    %% リレーションシップ
    User ||--o{ Order : "は複数の注文を持つ"
    User ||--o{ ShippingAddress : "は複数の配送先住所を登録できる"
    Order ||--|| ShippingAddress : "は1つの配送先住所を指定する"
    Order ||--o{ OrderItem : "は複数の注文明細を持つ"
    Product ||--o{ OrderItem : "は複数の注文明細に含まれる"
```
<img width="1470" height="824" alt="スクリーンショット 2026-02-16 23 46 14" src="https://github.com/user-attachments/assets/6f3bb71b-4bc9-439c-b272-d6eff9eb0bc6" />

