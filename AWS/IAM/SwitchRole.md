# スイッチロールの設定

## 目的
- rootユーザーの権限使用を避ける

## 参考
- [【AWS】スイッチロールで適切な権限付与を行う](https://zenn.dev/akkie1030/articles/aws-switch-role)

## 作業ログ

### ロール作成
- 信頼ポリシー
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```
- アクセスポリシー
  - `AdministarorAccess`を付与
https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-1#/roles/details/SwitchRoleAdministrator?section=permissions

- スイッチするユーザーを作成
  - 名前:`ecs_develop_user`
  - URL:https://730335441282.signin.aws.amazon.com/console

