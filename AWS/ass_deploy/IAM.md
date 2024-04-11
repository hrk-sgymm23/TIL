# IAMロール周りの設定

## 作成したリソース
### ロール
- `ecsTaskExecutionRole`

## 参考
- [Rails + React アプリを ECS Fargate にデプロイする【1. IAM編】](https://8tako8tako8.hatenablog.com/entry/2023/12/10/003507)

## ECS用の実行ロールを作成する

- AmazonECSTaskExecutionRolePolicy
- AmazonS3FullAccess
- AmazonSESFullAccess
- AmazonSSMFullAccess

上記を追加した`ecsTaskExecutionRole`を作成。
