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
 

## AWS_CLIでスイッチロール

### 認証情報よりアクセスキー発行

### クレデンシャル設定
```bash
aws configure
AWS Access Key ID [****************: xxx
AWS Secret Access Key [****************]: xxx
Default region name [ap-northeast-1]: ap-northeast-1
Default output format [json]: json
```

### 権限を試す
```bash
# ecs_developer...プロファイル名
$ export AWS_PROFILE=ecs_developer

$ aws s3 ls

An error occurred (AccessDenied) when calling the ListBuckets operation: Access Denied
```

### スイッチロールする
```bash
$ aws sts assume-role \
--role-arn "arn:aws:iam::730xxxxxxxxxx:role/{roleName}" \
--role-session-name "{switchRoleName}" \
--duration-seconds {3600} \
--profile {profile_name}


{
    "Credentials": {
        "AccessKeyId": "ASIxxxxxxL6EEI",
        "SecretAccessKey": "rIdbxxxxxxxxYYLxzD",
        "SessionToken": "FwoGZXxx6TtRkbs4KY4p1RkWGEh5osALuxxxxxxRGNiCorQELtxPpbVqsYgdbgXbzUsJBYWMXkvP65TV+NFadhsYhuO2RLvpwbg2DAxwcEC2FIHzfjjmSXEZoGKBVm+O8MfevLPbX6zIR8yi5BtFkzoSadjtsZzkF79LbFrZPWND46JRl1VvpJsnCJTKO4p52TXDX4e0vMvqHaRhQBF0hryoapDSiLWviuEj+AoxYXqsAYyLVaC2cB+m2otmqQffg80YHzNvoDfxocDA7pD+7MNNgbIehgMtmdXccqu0owc8A==",
        "Expiration": "2024-04-13T14:04:05+00:00"
    },
    "AssumedRoleUser": {
        "AssumedRoleId": "AROA2xxxxxQVXIL:SwitchRoleAdministrator",
        "Arn": "arn:aws:sts::730xxxxx:assumed-role/SwitchRoleAdministrator/SwitchRoleAdministrator"
    }
}
```

# 改修
`~/.aws/credential`
```bash
[ecs_developer]
aws_access_key_id = Axxxxxxxx
aws_secret_access_key = Dxxx
```

`~/.aws/config`
```bash
[profile ecs_developer]
region = ap-northeast-1
role_arn = arn:aws:iam::7303xxxx:role/SwitchRoleAdministrator
source_profile = ecs_developer
```

```bash
$ aws sts get-caller-identity --profile ecs_developer

{
    "UserId": "AROA2UC3COGBMHR3QVXIL:botocore-session-1713015486",
    "Account": "730xxxxxxx",
    "Arn": "arn:aws:sts::73sssss:assumed-role/SwitchRoleAdministrator/botocore-session-1713015486"
}
```

## 試す
```bash
$ aws s3 ls --profile ecs_developer
2024-03-20 20:55:13 ass-dev-bucket
```



