# ASSをECSを使ってデプロイ

## 参考
- [RailsとReactでSPA開発+AWS（Fargate・CloudFront）デプロイ解説チュートリアル
](https://zenn.dev/prune/books/28c2d690e11e45)
- [Rails + React アプリを ECS Fargate にデプロイする](https://8tako8tako8.hatenablog.com/entry/2023/12/10/003738)

## 作成するリソース群

## セキュリティ
- IAMユーザーとスイッチロール
  - https://blog.serverworks.co.jp/switch-role#%E5%B8%BD%E5%AD%90%E3%82%92%E3%81%8B%E3%81%B6%E3%81%A3%E3%81%A6%E5%8A%9B%E3%82%92%E5%BE%97%E3%82%8B
- ECS実行ロール

### ネットワーク
- VPC
- サブネット
- ロードバランサー(ALB)
- セキュリティグループ
- ルートテーブル
- インターネットゲートウェイ

### アプリケーション
- ECR
- ECS

### データベース
- RDS

