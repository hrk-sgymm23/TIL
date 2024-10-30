# FireStoreに定期的に書き込みに行くJobを作る

## 必要なリソース
- ArtifactRegistry
- CloudRun Jobs
- Sceduler
下記は今回既存のものを流用
- SerivceAccount(SecretManger,FireStore)
- SecretManger

## 必要な設定
- ArtifactRegistry
  - CloudRun用のサービスアカウントのアクセスを許可
- SecretManger
  - CloudRun用のサービスアカウントのアクセスを許可

## アプリケーションコードとDockerfileを用意
