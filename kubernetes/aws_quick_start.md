# EKS　クイックスタート

## `eksctl`インストール

```
$ brew install eksctl
```

## CLIの設定(STS)

https://qiita.com/SAITO_Keita/items/b29e1eb4792bab2d5f57#awsconfig%E3%81%A8awscredentials%E3%82%92%E5%88%A9%E7%94%A8%E3%81%99%E3%82%8B

上記を参考に実施

- CLI用のIAMユーザー作成
- スイッチ用のロールを作成
  - 上記で作成したアカウントIDを許可するassume付与
  - administoratoraccessを付与

### ロール用の信頼ポリシー
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::{IAMユーザーID}:user/runtarou_developer"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

