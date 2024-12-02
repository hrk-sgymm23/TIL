# Zennの気になる技術記事をレコメンドしてくれるやつを作る

## 要件

### 最重要要件
- 1日1回おきに技術ごとのトレンド記事から一記事抜粋し、その内容をようやくした文章をメールにて送信する。

### その他要件
- ようやくした内容をDynamoDBに対し保存
- DynamoDBから取得した情報を表示するサイトを作成
  - 上記に付随してAPIの作成の必要の可能性？

## 技術スタック

### AWS
- Lambda
- Event Bridge
- DynamoDB

### 言語
- Python
- Go

### ツール
- Gmail API
- Chatgpt API
- GitHubActions


## 参考
- [Pythonを使って、Gmailを送信する方法](https://note.com/noa813/n/nde0116fcb03f)
- [【AWS】Lambdaを使用しDynamoDBに読み書きする](https://zenn.dev/enumura/articles/71d88d98bc7052)
- [React + API Gateway + Lambda + DynamoDBでTodoアプリ](https://qiita.com/chain792/items/97d5dfd5a1b40ac63e05)
- [Github Actionsを使ってAWS Lambdaを自動デプロイしてみた](https://qiita.com/hasesho/items/c5100eeb3393b412d816)
- [【X(Twitter) Bot】Ｘの運用がめんどくさい全ての人へ](https://zenn.dev/enterrocken/articles/e6ae6ddcc121d8)
